cmake_minimum_required(VERSION 3.25 FATAL_ERROR)

project(conccpp LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED YES)
set(CMAKE_CXX_EXTENSIONS NO)

include(CTest)
include(cmake/SetupCompilerWarnings.cmake)

add_subdirectory(third_party)
add_subdirectory(queue)
