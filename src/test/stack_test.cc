#include "concpp/stack.h"

#include <string>

#include "gtest/gtest.h"

namespace {

TEST(Stack, PopOnNewInstanceReturnsEmptyOptional) {
  concpp::stack<int> stack;
}

}  // namespace

