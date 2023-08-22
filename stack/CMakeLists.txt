add_library(
  concpp_stack
  src/concpp/stack.cc
)

target_include_directories(
  concpp_stack
  PUBLIC
  "include"
)

if(BUILD_TESTING)
  add_subdirectory(test)
endif()
