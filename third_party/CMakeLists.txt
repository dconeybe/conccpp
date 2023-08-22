list(APPEND CMAKE_MESSAGE_CONTEXT "third_party")

if(BUILD_TESTING)
  add_subdirectory(googletest)
endif()
