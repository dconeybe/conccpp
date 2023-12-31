block()

include(CheckCXXCompilerFlag)
include(ConcppGetValueForCompiler)

list(APPEND CMAKE_MESSAGE_CONTEXT "ConcppSetupCompilerWarnings")

set(all_warning_flags_gnu
  -Wall
  -Wextra
  -pedantic
  -Wcast-align
  -Wconditional-uninitialized
  -Wconversion
  -Wdouble-promotion
  -Wduplicated-branches
  -Wduplicated-cond
  -Weffc++
  -Wformat=2
  -Wimplicit-fallthrough
  -Winfinite-recursion
  -Wlifetime
  -Wlogical-op
  -Wmove
  -Wmisleading-indentation
  -Wnon-virtual-dtor
  -Wnull-dereference
  -Wold-style-cast
  -Woverloaded-virtual
  -Wpedantic
  -Wreorder
  -Wrange-loop-analysis
  -Wreturn-type
  -Wshadow
  -Wsign-conversion
  -Wuninitialized
  -Wunreachable-code
  -Wunused
  -Wuseless-cast
)

set(all_warning_flags_msvc
  /permissive
  /W4
  /wd4146
  /wd4566
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

ConcppGetValueForCompiler(
  "all_warning_flags"
  "${all_warning_flags_gnu}"
  "${all_warning_flags_msvc}"
  "NOTFOUND"
)

if(NOT all_warning_flags)
  unset(all_warning_flags)
  message(
    NOTICE
    "Compiler flags for enabling warnings for the current compiler are not known; "
    "not adding compiler flags to enable warnings."
  )
endif()

# Test each flag for compiler support and create a list of *supported* warning flags.
set(supported_warning_flags "")
set(all_warning_flags_cache_vars "")
foreach(warning_flag IN LISTS all_warning_flags)
  # Maps each warning flag to a unique cache variable.
  set(warning_flag_id "${warning_flag}")
  string(REPLACE "/" "" warning_flag_id "${warning_flag_id}")
  string(REPLACE "-" "" warning_flag_id "${warning_flag_id}")
  string(REPLACE "=" "" warning_flag_id "${warning_flag_id}")
  string(REPLACE "++" "pp" warning_flag_id "${warning_flag_id}")
  set(warning_flag_cache_var "CONCPP_COMPILER_WARNING_${warning_flag_id}")

  # Verify that the mapping is unique.
  list(FIND all_warning_flags_cache_vars "${warning_flag_cache_var}" "warning_flag_cache_var_index")
  if(warning_flag_cache_var_index GREATER_EQUAL 0)
    list(GET all_warning_flags "${warning_flag_cache_var_index}" existing_warning_flag)
    message(
      FATAL_ERROR
      "INTERNAL ERROR: Both warning flags ${existing_warning_flag} and ${warning_flag} "
      "map to the same cache variable: ${warning_flag_cache_var}"
    )
  endif()
  list(APPEND all_warning_flags_cache_vars "${warning_flag_cache_var}")

  # Test the compiler for support of the current warning flag.
  message(VERBOSE "Testing for compiler support of flag: ${warning_flag}")
  check_cxx_compiler_flag("${warning_flag}" "${warning_flag_cache_var}")
  if(${warning_flag_cache_var})
    list(APPEND supported_warning_flags "${warning_flag}")
  endif()
endforeach()

# Set the supported warnings.
string(JOIN ", " supported_warning_flags_str ${supported_warning_flags})
message(VERBOSE "Setting compiler warning flags: ${supported_warning_flags_str}")
add_compile_options(${supported_warning_flags})

endblock()
