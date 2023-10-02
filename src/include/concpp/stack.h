#ifndef CONCPP_STACK_H_
#define CONCPP_STACK_H_

#include <atomic>
#include <optional>
#include <utility>

namespace concpp {

/**
 * A stack data structure that is lock-free.
 *
 * The `head_` pointer always points to a non-null object. Initially, it points to a "sentinel"
 * object. The "sentinel" can be identified because its `next` pointer is `nullptr`.
 */
template <typename T>
class LockFreeStack final {
 public:
  ~LockFreeStack() {
    Node* head = head_.load();
    while (head) {
      Node* next = head->next;
      delete head;
      head = next;
    }
  }

  void push(T value) {
    auto* new_node = new Node(std::move(value), head_.load());
    while (!head_.compare_exchange_weak(new_node->next, new_node))
      ;
  }

  std::optional<T> pop() {
    Node* old_head = head_.load();
    while (true) {
      if (!old_head->valid) {
        return std::nullopt;
      }
      if (head_.compare_exchange_weak(old_head, old_head->next)) {
        break;
      }
    }
    return std::move(*old_head).value();
  }

 private:
  struct Node {
    Node() = default;
    Node(const Node&) = delete;
    Node& operator=(const Node&) = delete;

    Node(T value, Node* next_) : valid(true), next(next_) {
      new (value_) T(std::move(value));
    }

    ~Node() {
      if (valid) {
        value().~T();
      }
    }

    const T& value() const& {
      return *reinterpret_cast<const T*>(value_);
    }

    T& value() & {
      return *reinterpret_cast<T*>(value_);
    }

    T&& value() && {
      return std::move(*reinterpret_cast<T*>(value_));
    }

    bool valid = false;
    Node* next = nullptr;
    alignas(T) char value_[sizeof(T)]{};
  };

  std::atomic<Node*> head_ = new Node;
};

}  // namespace concpp

#endif  // CONCPP_STACK_H_