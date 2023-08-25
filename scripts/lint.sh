#!/bin/bash

set -euo pipefail

readonly pyflakes_args=(
  pyflakes
  cmake/test/*.py
  workflows/checks/*.py
  "$@"
)

echo "${pyflakes_args[*]}"
exec "${pyflakes_args[@]}"
