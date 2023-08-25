function(ConcppGetValueForCompiler OUTVAR GCC_VALUE MSVC_VALUE DEFAULT_VALUE)
  list(APPEND CMAKE_MESSAGE_CONTEXT "GetValueForCompiler")

  if(ARGC GREATER 4)
    list(JOIN ARGN ", " ARGN_STR)
    message(
      FATAL_ERROR
      "${CMAKE_CURRENT_FUNCTION} was invoked with ${ARGC} arguments, but exactly 4 expected "
      "(unexpected arguments: ${ARGN_STR})"
    )
  endif()

  message(VERBOSE "CMAKE_CXX_COMPILER_FRONTEND_VARIANT=${CMAKE_CXX_COMPILER_FRONTEND_VARIANT}")
  message(VERBOSE "CMAKE_CXX_COMPILER_ID=${CMAKE_CXX_COMPILER_ID}")

  # Determine the "flavor" of warning flags to used based on the compiler cmake is using.
  if(CMAKE_CXX_COMPILER_FRONTEND_VARIANT)
    if(CMAKE_CXX_COMPILER_FRONTEND_VARIANT STREQUAL "GNU")
      set(detected_compiler "gcc")
    elseif(CMAKE_CXX_COMPILER_FRONTEND_VARIANT MATCHES "Clang")
      set(detected_compiler "gcc")
    elseif(CMAKE_CXX_COMPILER_FRONTEND_VARIANT STREQUAL "MSVC")
      set(detected_compiler "msvc")
    else()
      unset(detected_compiler)
    endif()
  elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
    set(detected_compiler "gcc")
  elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
    set(detected_compiler "gcc")
  elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
    set(detected_compiler "msvc")
  else()
    unset(detected_compiler)
  endif()

  # Return the value corresponding to the detected compiler.
  if(detected_compiler STREQUAL "gcc")
    set(result "${GCC_VALUE}")
  elseif(detected_compiler STREQUAL "msvc")
    set(result "${MSVC_VALUE}")
  elseif(detected_compiler)
    message(
      FATAL_ERROR
      "internal error: unexpected value for `detected_compiler`: ${detected_compiler}"
    )
  else()
    set(result "${DEFAULT_VALUE}")
  endif()

  set("${OUTVAR}" "${result}" PARENT_SCOPE)
endfunction()
