include(../../cmake/GetUserHomeDir.cmake)

list(APPEND CMAKE_MESSAGE_CONTEXT "googletest")

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
