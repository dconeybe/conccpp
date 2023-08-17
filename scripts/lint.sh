#!/bin/bash

set -euo pipefail

readonly pyflakes_args=(
  pyflakes
  cmake/*.py
  "$@"
)

echo "${pyflakes_args[*]}"
exec "${pyflakes_args[@]}"
