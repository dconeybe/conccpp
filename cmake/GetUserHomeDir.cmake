function(GetUserHomeDir OUTVAR)
  list(APPEND CMAKE_MESSAGE_CONTEXT "GetUserHomeDir")

  if(ARGC GREATER 1)
    list(JOIN ARGN ", " ARGN_STR)
    message(
      FATAL_ERROR
      "${CMAKE_CURRENT_FUNCTION} was invoked with ${ARGC} arguments, but exactly 1 expected "
      "(unexpected arguments: ${ARGN_STR})"
    )
  endif()

  if(CMAKE_HOST_WIN32)
    set(user_home "$ENV{USERPROFILE}")
  else()
    set(user_home "$ENV{HOME}")
  endif()

  if(user_home)
    set("${OUTVAR}" "${user_home}" PARENT_SCOPE)
  else()
    set("${OUTVAR}" "NOTFOUND" PARENT_SCOPE)
  endif()
endfunction()
