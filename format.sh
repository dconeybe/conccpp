#!/bin/bash

set -euo pipefail

readonly pyink_args=(
  pyink
  --line-length 100
  --target-version py311
  --pyink
  --pyink-indentation 2
  cmake/*.py
  "$@"
)

echo "${pyink_args[*]}"
exec "${pyink_args[@]}"
