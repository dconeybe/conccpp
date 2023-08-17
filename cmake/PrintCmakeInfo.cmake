block()

list(APPEND CMAKE_MESSAGE_CONTEXT "PrintCmakeInfo")

set(vars "")
list(APPEND vars "CMAKE_COMMAND")
list(APPEND vars "CMAKE_VERSION")
list(APPEND vars "CMAKE_GENERATOR")
list(APPEND vars "CMAKE_MAKE_PROGRAM")
list(APPEND vars "CMAKE_BUILD_TYPE")
list(APPEND vars "CMAKE_CXX_COMPILER_ID")
list(APPEND vars "CMAKE_CXX_COMPILER_VERSION")
list(APPEND vars "CMAKE_CXX_COMPILER_FRONTEND_VARIANT")
list(APPEND vars "CMAKE_CXX_COMPILER")
list(APPEND vars "CMAKE_CXX_BYTE_ORDER")
list(APPEND vars "CMAKE_HOST_SYSTEM_NAME")
list(APPEND vars "CMAKE_HOST_SYSTEM_PROCESSOR")
list(APPEND vars "CMAKE_HOST_SYSTEM_VERSION")
list(APPEND vars "CMAKE_SYSTEM_NAME")
list(APPEND vars "CMAKE_SYSTEM_PROCESSOR")
list(APPEND vars "CMAKE_SYSTEM_VERSION")

foreach(var IN LISTS vars)
  message("${var}=${${var}}")
endforeach()

endblock()
