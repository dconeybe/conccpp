include(../../cmake/GetUserHomeDir.cmake)

list(APPEND CMAKE_MESSAGE_CONTEXT "googletest")

set(download_file "61332bd7e8810edd7ff9febfa71ece2e25b18df0.zip")
set(download_url "https://github.com/google/googletest/archive/${download_file}")
set(download_expected_sha512 "cf0c55a3ace208e7f796efec44ca08f4d04d3798888f703cf3b371b2a56e339ece38364a3acea8eedb53cb9ceb896b9aba3ec08637133b9072cfa8af0a19ae24")
string(LENGTH "${download_expected_sha512}" "download_sha512_length")
set(expected_stamp_file_contents "${download_expected_sha512}")
set(googletest_extract_dir "${CMAKE_CURRENT_BINARY_DIR}/extract")
set(googletest_source_dir "${CMAKE_CURRENT_BINARY_DIR}/src")
set(googletest_binary_dir "${CMAKE_CURRENT_BINARY_DIR}/build")

set(stamp_file "${CMAKE_CURRENT_BINARY_DIR}/stamp.txt")
if(NOT EXISTS "${stamp_file}")
  message(VERBOSE "Stamp file not found: ${stamp_file}")
  message(VERBOSE "Proceeding with download and extract")
  set(do_download_and_extract YES)
else()
  message(VERBOSE "Reading stamp file: ${stamp_file}")
  math(EXPR stamp_file_read_limit "${download_sha512_length}+1")
  file(READ "${stamp_file}" stamp_file_contents LIMIT "${stamp_file_read_limit}")
  if(stamp_file_contents STREQUAL expected_stamp_file_contents)
    set(do_download_and_extract NO)
    message(VERBOSE "Stamp file contained the expected contents; skipping download and extract")
  else()
    set(do_download_and_extract YES)
    message(
      VERBOSE
      "Stamp file contained unexpected contents: ${stamp_file_contents} "
      "(expected: ${expected_stamp_file_contents}); proceeding with download and extract"
    )
  endif()
endif()

if(do_download_and_extract)
  include(../../cmake/GetUserHomeDir.cmake)
  GetUserHomeDir(home_dir)

  option(
    CONCPP_DOWNLOAD_CACHE_ENABLED
    "Whether to cache downloaded files locally"
    YES
  )

  set(
    CONCPP_DOWNLOAD_CACHE_DIR
    "${home_dir}/.concpp_download_cache"
    CACHE
    PATH
    "The directory in which downloaded files will be cached"
  )

  if(CONCPP_DOWNLOAD_CACHE_ENABLED)
    message(
      VERBOSE
      "Download cache is enabled (CONCPP_DOWNLOAD_CACHE_ENABLED=${CONCPP_DOWNLOAD_CACHE_ENABLED})"
    )
    message(
      VERBOSE
      "Download cache directory: CONCPP_DOWNLOAD_CACHE_DIR=${CONCPP_DOWNLOAD_CACHE_DIR}"
    )
  set(download_dest_file "${CONCPP_DOWNLOAD_CACHE_DIR}/${download_file}")
  else()
    message(
      VERBOSE
      "Download cache is disabled (CONCPP_DOWNLOAD_CACHE_ENABLED=${CONCPP_DOWNLOAD_CACHE_ENABLED})"
    )
    set(download_dest_file "${CMAKE_CURRENT_BINARY_DIR}/${download_file}")
  endif()

  cmake_path(GET download_dest_file PARENT_PATH download_dest_dir)
  if(NOT EXISTS "${download_dest_dir}")
    message(VERBOSE "Creating directory: ${download_dest_dir}")
    file(MAKE_DIRECTORY "${download_dest_dir}")
  endif()

  if(NOT EXISTS "${download_dest_file}")
    message(VERBOSE "Previously-downloaded file not found: ${download_dest_file}")
    set(do_download YES)
  else()
    message(VERBOSE "Previously-downloaded file exists: ${download_dest_file}")
    message(VERBOSE "Verifying SHA512 hash of previously-downloaded file: ${download_dest_file}")
    file(SHA512 "${download_dest_file}" "download_dest_file_sha512")
    if(download_dest_file_sha512 STREQUAL download_expected_sha512)
      message(
        VERBOSE
        "SHA512 hash of ${download_dest_file} equals the expected hash; "
        "skipping download and re-using the previously-downloaded file"
      )
      set(do_download NO)
    else()
      message(
        VERBOSE
        "SHA512 hash of ${download_dest_file} does NOT equal the expected hash: "
        "${download_dest_file_sha512} (expected ${download_expected_sha512}); "
        "discarding previously-downloaded file and re-downloading"
      )
      set(do_download YES)
    endif()
  endif()

  if(do_download)
    message("Downloading ${download_url} to ${download_dest_file}")
    file(
      DOWNLOAD
      "${download_url}"
      "${download_dest_file}"
      EXPECTED_HASH
      "SHA512=${download_expected_sha512}"
    )
  endif()

  if(EXISTS "${googletest_extract_dir}")
    message(VERBOSE "Deleting directory: ${googletest_extract_dir}")
    file(REMOVE_RECURSE "${googletest_extract_dir}")
  endif()

  message(VERBOSE "Extracting ${download_dest_file} to ${googletest_extract_dir}")
  file(
    ARCHIVE_EXTRACT
    INPUT "${download_dest_file}"
    DESTINATION "${googletest_extract_dir}"
  )

  file(GLOB googletest_extract_dir_entries "${googletest_extract_dir}/*")
  list(LENGTH googletest_extract_dir_entries "googletest_extract_dir_entries_length")
  if(NOT googletest_extract_dir_entries_length EQUAL 1)
    message(
      FATAL_ERROR
      "Extracting ${download_url} produced ${googletest_extract_dir_entries_length} entries in "
      "directory ${googletest_extract_dir}, but expected exactly 1"
    )
  endif()
  list(GET googletest_extract_dir_entries 0 googletest_extract_dir_entry)

  if(EXISTS "${googletest_source_dir}")
    message(VERBOSE "Deleting directory: ${googletest_source_dir}")
    file(REMOVE_RECURSE "${googletest_source_dir}")
  endif()

  message(VERBOSE "Creating directory: ${googletest_source_dir}")
  file(MAKE_DIRECTORY "${googletest_source_dir}")

  file(GLOB googletest_extract_subdir_entries "${googletest_extract_dir_entry}/*")
  foreach(googletest_extract_subdir_entry IN LISTS googletest_extract_subdir_entries)
    message(VERBOSE "Moving ${googletest_extract_subdir_entry} to ${googletest_source_dir}")
    cmake_path(GET googletest_extract_subdir_entry FILENAME cur_filename)
    file(RENAME "${googletest_extract_subdir_entry}" "${googletest_source_dir}/${cur_filename}")
  endforeach()

  if(EXISTS "${googletest_binary_dir}")
    message(VERBOSE "Deleting directory: ${googletest_binary_dir}")
    file(REMOVE_RECURSE "${googletest_binary_dir}")
  endif()

  message(VERBOSE "Creating stamp file: ${stamp_file}")
  file(WRITE "${stamp_file}" "${expected_stamp_file_contents}")
endif()

add_subdirectory(
  "${googletest_source_dir}"
  "${googletest_binary_dir}"
  SYSTEM
  EXCLUDE_FROM_ALL
)
