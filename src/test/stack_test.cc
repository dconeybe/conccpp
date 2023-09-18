#include "concpp/stack.h"

#include <algorithm>
#include <latch>
#include <thread>
#include <vector>

#include "gtest/gtest.h"

namespace {

void test_concurrent_push_and_pop_threads(unsigned push_thread_count, unsigned pop_thread_count) {
  concpp::stack<int> stack;
  std::latch latch(push_thread_count + pop_thread_count);
  std::vector<std::thread> threads(push_thread_count + pop_thread_count);

  std::vector<std::vector<int>> popped_values_by_thread;
  for (unsigned i=0; i<pop_thread_count; i++) {
    popped_values_by_thread.emplace_back();
  }

  const std::vector<int> expected_popped_values = [push_thread_count]{
    std::vector<int> values;
    for (int popped_value=0; popped_value<10'000; popped_value++) {
      for (unsigned push_thread_index=0; push_thread_index<push_thread_count; push_thread_index++) {
        values.push_back(popped_value);
      }
    }
    return values;
  }();
  std::atomic<unsigned> popped_values_count{0};

  // Save `expected_popped_values.size()` to an int local variable to avoid a data race between the popper threads and
  // the vector's destructor, which is run on this thread.
  const auto max_expected_popped_values_count = expected_popped_values.size();

  for (unsigned i=0; i<push_thread_count; i++) {
    threads.emplace_back([&] {
      latch.arrive_and_wait();
      for (int i=0; i<10'000; i++) {
        stack.push(i);
      }
    });
  }

  for (unsigned i=0; i<pop_thread_count; i++) {
    std::vector<int>& popped_values = popped_values_by_thread[i];
    threads.emplace_back([&] {
      latch.arrive_and_wait();
      while (true) {
        std::unique_ptr<int> popped_value = stack.pop();
        if (popped_value) {
          popped_values.push_back(*popped_value);
          popped_values_count.fetch_add(1, std::memory_order_relaxed);
        } else if (popped_values_count.load(std::memory_order_relaxed) >= max_expected_popped_values_count) {
          break;
        }
      }
    });
  }

  for (std::thread& thread : threads) {
    thread.join();
  }

  std::vector<int> popped_values;
  for (const std::vector<int>& cur_popped_values : popped_values_by_thread) {
    for (int popped_value : cur_popped_values) {
      popped_values.push_back(popped_value);
    }
  }

  std::sort(popped_values.begin(), popped_values.end());

  EXPECT_EQ(popped_values, expected_popped_values);
}

TEST(Stack, PopOnNewInstanceReturnsNull) {
  concpp::stack<int> stack;

  std::unique_ptr<int> result = stack.pop();

  EXPECT_FALSE(result);
}

TEST(Stack, PushThenPopOneValue) {
  concpp::stack<int> stack;
  stack.push(42);

  std::unique_ptr<int> result = stack.pop();

  ASSERT_TRUE(result);
  EXPECT_EQ(*result, 42);
}

TEST(Stack, PushThenPop100Values) {
  concpp::stack<int> stack;
  for (int i=0; i<100; i++) {
    stack.push(i);
  }

  for (int i=0; i<100; i++) {
    SCOPED_TRACE("i=" + std::to_string(i));
    std::unique_ptr<int> result = stack.pop();
    ASSERT_TRUE(result);
    EXPECT_EQ(*result, 99-i);
  }
}

TEST(Stack, ConcurrentPushAndPopSinglePushThreadSinglePopThread) {
  test_concurrent_push_and_pop_threads(/*push_thread_count=*/1, /*pop_thread_count=*/1);
}

TEST(Stack, ConcurrentPushAndPop4PushThreads4PopThreads) {
  test_concurrent_push_and_pop_threads(/*push_thread_count=*/4, /*pop_thread_count=*/4);
}

}  // namespace

