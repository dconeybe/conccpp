#include "concpp/stack.h"

#include <algorithm>
#include <latch>
#include <mutex>
#include <thread>
#include <vector>

#include "gtest/gtest.h"

namespace {

/**
 * Run a test that launches threads to concurrently call push() and pop() on a stack.
 * Fails the current test if anything other than the exact values that were pushed are popped.
 *
 * @param push_thread_count the number of threads to launch to call push().
 * @param pop_thread_count the number of threads to launch to call pop().
 */
void test_concurrent_push_and_pop_threads(unsigned push_thread_count, unsigned pop_thread_count);

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

void test_concurrent_push_and_pop_threads(unsigned push_thread_count, unsigned pop_thread_count) {
  concpp::stack<int> stack;
  std::latch latch(push_thread_count + pop_thread_count);
  std::vector<std::thread> threads;

  std::mutex popped_values_mutex;
  std::vector<int> popped_values;

  const std::vector<int> expected_popped_values = [push_thread_count]{
    std::vector<int> values;
    for (int popped_value=0; popped_value<100'000; popped_value++) {
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

  // Create the "pusher" threads.
  // Each pushed thread pushes a bunch of values onto the stack.
  for (unsigned i=0; i<push_thread_count; i++) {
    threads.emplace_back([&] {
      latch.arrive_and_wait();
      for (int i=0; i<100'000; i++) {
        stack.push(i);
      }
    });
  }

  // Create the "popper" threads.
  // Each popper thread repeatedly pops a value off of the stack.
  for (unsigned i=0; i<pop_thread_count; i++) {
    threads.emplace_back([&] {
      // Create a vector into which the values popped by this thread will be stored.
      std::vector<int> my_popped_values;

      // Wait until all pusher and popper threads are alive and ready.
      latch.arrive_and_wait();

      while (true) {
        std::unique_ptr<int> popped_value = stack.pop();

        // Append the value popped from the stack into our vector.
        // Also, increment the count of popped values from all threads.
        if (popped_value) {
          my_popped_values.push_back(*popped_value);
          popped_values_count.fetch_add(1, std::memory_order_relaxed);

          // Break out of the loop if the number of popped values from all popper threads has reached the expected count.
        } else if (popped_values_count.load(std::memory_order_relaxed) >= max_expected_popped_values_count) {
          break;
        }
      }

      // Update the shared vector with the values that were popped by this thread.
      // Do this _after_ we're doing popping to avoid costly synchronization during the "pop" loop.
      std::lock_guard<std::mutex> lock(popped_values_mutex);
      for (int popped_value : my_popped_values) {
        popped_values.push_back(popped_value);
      }
    });
  }

  // Wait for the pusher and popper threads to complete.
  for (std::thread& thread : threads) {
    thread.join();
  }

  // Sort the popped values so that they can be compared with the "expected" vector of popped values.
  std::sort(popped_values.begin(), popped_values.end());

  // Make sure the exact set of expected popped values was actually popped.
  EXPECT_EQ(popped_values, expected_popped_values);
}

}  // namespace

