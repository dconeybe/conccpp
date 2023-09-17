add_executable(
  concpp_test
  stack_test.cc
)

add_test(concpp_test concpp_test)

target_link_libraries(
  concpp_test
  PRIVATE
  concpp
  gmock_main
)
