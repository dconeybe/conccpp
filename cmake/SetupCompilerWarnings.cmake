block()

include(CheckCXXCompilerFlag)

list(APPEND CMAKE_MESSAGE_CONTEXT "SetupCompilerWarnings")

message(VERBOSE "CMAKE_CXX_COMPILER_FRONTEND_VARIANT=${CMAKE_CXX_COMPILER_FRONTEND_VARIANT}")
message(VERBOSE "CMAKE_CXX_COMPILER_ID=${CMAKE_CXX_COMPILER_ID}")

# Determine the "flavor" of warning flags to used based on the compiler cmake is using.
if(CMAKE_CXX_COMPILER_FRONTEND_VARIANT)
  if(CMAKE_CXX_COMPILER_FRONTEND_VARIANT STREQUAL "GNU")
    set(warning_flags_id "warning_flags_gnu")
  elseif(CMAKE_CXX_COMPILER_FRONTEND_VARIANT MATCHES "Clang")
    set(warning_flags_id "warning_flags_gnu")
  elseif(CMAKE_CXX_COMPILER_FRONTEND_VARIANT STREQUAL "MSVC")
    set(warning_flags_id "warning_flags_msvc")
  else()
    set(warning_flags_id "warning_flags_unknown")
    message(
      NOTICE
      "Compiler options for enabling warnings for "
      "CMAKE_CXX_COMPILER_FRONTEND_VARIANT=${CMAKE_CXX_COMPILER_FRONTEND_VARIANT} "
      "are not known; not adding compiler flags to enable warnings."
    )
  endif()
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "GNU")
  set(warning_flags_id "warning_flags_gnu")
elseif(CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  set(warning_flags_id "warning_flags_gnu")
elseif(CMAKE_CXX_COMPILER_ID STREQUAL "MSVC")
  set(warning_flags_id "warning_flags_msvc")
else()
  set(warning_flags_id "warning_flags_unknown")
  message(
    NOTICE
    "Compiler options for enabling warnings for "
    "CMAKE_CXX_COMPILER_ID=${CMAKE_CXX_COMPILER_ID} "
    "are not known; not adding compiler flags to enable warnings."
  )
endif()

# Determine the actual flags to set for the detected compiler.
if(warning_flags_id STREQUAL "warning_flags_gnu")
  set(all_warning_flags
    -Wall
    -Wextra
    -pedantic
    -Wcast-align
    -Wconversion
    -Wdouble-promotion
    -Wduplicated-branches
    -Wduplicated-cond
    -Weffc++
    -Wformat=2
    -Wimplicit-fallthrough
    -Wlifetime
    -Wlogical-op
    -Wmisleading-indentation
    -Wnon-virtual-dtor
    -Wnull-dereference
    -Wold-style-cast
    -Woverloaded-virtual
    -Wpedantic
    -Wshadow
    -Wsign-conversion
    -Wunused
    -Wuseless-cast
  )
elseif(warning_flags_id STREQUAL "warning_flags_msvc")
  set(all_warning_flags
    /permissive
    /W4
    /w14242
    /w14254
    /w14263
    /w14265
    /w14287
    /w14296
    /w14311
    /w14545
    /w14546
    /w14547
    /w14549
    /w14555
    /w14619
    /w14640
    /w14826
    /w14905
    /w14906
    /w14928
    /we4289
  )
elseif(warning_flags_id STREQUAL "warning_flags_unknown")
  set(all_warning_flags "")
else()
  message(
    FATAL_ERROR
    "INTERNAL ERROR: unrecognized value for `warning_flags_id` variable: ${warning_flags_id}"
  )
endif()

# Test each option for compiler support and create a list of *supported* warning options.
set(supported_warning_flags "")
set(all_warning_flag_cache_vars "")
foreach(warning_flag IN LISTS all_warning_flags)
  # Maps each warning option to a unique cache variable.
  set(warning_flag_id "${warning_flag}")
  string(REPLACE "/" "" warning_flag_id "${warning_flag_id}")
  string(REPLACE "-" "" warning_flag_id "${warning_flag_id}")
  string(REPLACE "=" "" warning_flag_id "${warning_flag_id}")
  string(REPLACE "++" "pp" warning_flag_id "${warning_flag_id}")
  set(warning_flag_cache_var "CONCPP_COMPILER_WARNING_${warning_flag_id}")

  # Verify that the mapping is unique.
  list(FIND all_warning_flag_cache_vars "${warning_flag_cache_var}" "warning_flag_cache_var_index")
  if(warning_flag_cache_var_index GREATER_EQUAL 0)
    list(GET all_warning_flags "${warning_flag_cache_var_index}" existing_warning_flag)
    message(
      FATAL_ERROR
      "INTERNAL ERROR: Both warning flags ${existing_warning_flag} and ${warning_flag} "
      "map to the same cache variable: ${warning_flag_cache_var}"
    )
  endif()
  list(APPEND all_warning_flag_cache_vars "${warning_flag_cache_var}")

  # Test the compiler for support of the current warning option.
  message(VERBOSE "Testing for compiler support of option: ${warning_flag}")
  check_cxx_compiler_flag("${warning_flag}" "${warning_flag_cache_var}")
  if(${warning_flag_cache_var})
    list(APPEND supported_warning_flags "${warning_flag}")
  endif()
endforeach()

# Set the supported warnings.
string(JOIN ", " supported_warning_flags_str ${supported_warning_flags})
message(VERBOSE "Setting compiler warning flags: ${supported_warning_flags_str}")
add_compile_options(${supported_warning_flags_str})

endblock()
