#include "concpp/stack.h"

#include <string>

#include "gtest/gtest.h"

using concpp::LockFreeStack;

namespace {

TEST(Stack, PopOnNewInstanceReturnsEmptyOptional) {
  LockFreeStack<int> stack;
  EXPECT_FALSE(stack.pop());
  EXPECT_FALSE(stack.pop());
  EXPECT_FALSE(stack.pop());
  EXPECT_FALSE(stack.pop());
}

TEST(Stack, PushOnNewInstancePushesTheValue) {
  LockFreeStack<int> stack;
  stack.push(42);

  std::optional<int> value = stack.pop();

  ASSERT_TRUE(value.has_value());
  EXPECT_EQ(value.value(), 42);
}

TEST(Stack, PushABunchThenPopThen) {
  LockFreeStack<int> stack;
  for (int i = 0; i < 5; i++) {
    stack.push(i);
  }

  for (int i = 4; i >= 0; i--) {
    SCOPED_TRACE("i=" + std::to_string(i));
    std::optional<int> value = stack.pop();
    ASSERT_TRUE(value.has_value());
    EXPECT_EQ(value.value(), i);
  }
}

}  // namespace
