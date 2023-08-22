#include "concpp/stack.h"

#include "gtest/gtest.h"

using concpp::LockFreeStack;

namespace {

TEST(Stack, Push3Pop3Int) {
  LockFreeStack<int> stack;
  for (int i=0; i<5; i++) {
    stack.push(i);
  }
  for (int i=4; i>=0; i--) {
    EXPECT_EQ(stack.pop().value(), i);
  }
}

}  // namespace

