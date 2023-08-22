#ifndef CONCPP_STACK_H_
#define CONCPP_STACK_H_

#include <atomic>
#include <optional>
#include <utility>

namespace concpp {

template<typename T>
class LockFreeStack final {
public:
  void push(T value) {
    auto *new_node = new Node;
    new(new_node->value) T(std::move(value));
    new_node->next = head_.load();
    while (!head_.compare_exchange_weak(new_node->next, new_node));
  }

  std::optional<T> pop() {
    Node *old_head = head_.load();
    while (true) {
      if (old_head->next == nullptr) {
        return std::nullopt;
      }
      if (head_.compare_exchange_weak(old_head, old_head->next)) {
        break;
      }
    }
    return T(std::move(*reinterpret_cast<T *>(old_head->value)));
  }

private:
  struct Node {
    alignas(T) char value[sizeof(T)];
    Node *next = nullptr;
  };

  std::atomic<Node *> head_ = new Node;
};

} // namespace concpp

#endif  // CONCPP_STACK_H_