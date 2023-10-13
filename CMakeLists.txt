cmake_minimum_required(VERSION 3.25 FATAL_ERROR)
asdf
project(conccpp LANGUAGES CXX)

list(APPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake")

option(CONCPP_LOG_CMAKE_INFO "Log interesting cmake variables" NO)
if(CONCPP_LOG_CMAKE_INFO)
  include(ConcppPrintCmakeInfo)
endif()

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED YES)
set(CMAKE_CXX_EXTENSIONS NO)

include(CTest)

add_subdirectory(third_party)

# Add compiler warning flags _after_ including `third_party` so that we don't get spurious
# warnings from third-party code.
include(ConcppSetupCompilerWarnings)

add_subdirectory(src)
