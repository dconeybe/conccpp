add_executable(
  concpp_stack_test
  stack_test.cc
)

add_test(concpp_stack_test concpp_stack_test)

target_link_libraries(
  concpp_stack_test
  PRIVATE
  concpp_stack
  gmock_main
)
