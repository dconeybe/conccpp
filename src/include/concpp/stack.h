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

  void push(std::unique_ptr<T> data) {
    // Create the new node to put onto the top of the stack; initialize its "next" pointer to whatever the current
    // "head" node is.
    node* new_head = new node;
    new_head->data = std::move(data);
    new_head->next = head_.load();

    // Replace the current "head" node with the new node. If the "head" node changed since the last time we read it then
    // update the "next" pointer to the new head (as a side effect of `compare_exchange_weak()`) and try again.
    while (!head_.compare_exchange_weak(new_head->next, new_head));
  }

  std::unique_ptr<T> pop() {
    node* head = head_.load();
    while (true) {
      // Return a "null" value if this stack is empty, which is indicated by the "next" pointer of "head" being null.
      if (!head->next) {
        return {};
      }

      if (head_.compare_exchange_strong(head, head->next)) {
        // TODO: Delete the `head` node, which is currently leaking.
        return std::move(head->data);
      }
    }
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