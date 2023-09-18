#ifndef CONCPP_STACK_H_
#define CONCPP_STACK_H_

#include <atomic>
#include <memory>
#include <type_traits>
#include <utility>

namespace concpp {

template<typename T>
class stack final {
 public:
  stack() : head_(new node) {
  }

  ~stack() {
    node* head = head_.load();
    while (true) {
      if (!head) {
        break;
      }
      node* next = head->next;
      delete head;
      head = next;
    }
  }

  void push(T value) {
    return push(std::make_unique<T>(std::move(value)));
  }

  void push(std::unique_ptr<T>) {

  }

  std::unique_ptr<T> pop() {
    return {};
  }

  // Move and delete copy constructors and assignment operators are not supported.
  stack(const stack&) = delete;
  stack(stack&&) = delete;
  stack& operator=(const stack&) = delete;
  stack& operator=(stack&&) = delete;

 private:
  struct node {
    std::unique_ptr<T> data;
    node* next = nullptr;
  }; // class node

  [[maybe_unused]]
  void type_traits_static_asserts() {
    static_assert(decltype(head_)::is_always_lock_free);
  }

  std::atomic<node*> head_;
}; // class stack

} // namespace concpp

#endif  // CONCPP_STACK_H_