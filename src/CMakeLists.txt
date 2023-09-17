add_library(
  concpp
  dummy.cc
)

target_include_directories(
  concpp
  PUBLIC
  include
)

if(BUILD_TESTING)
  add_subdirectory(test)
endif()
