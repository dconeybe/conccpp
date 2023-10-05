#!/bin/sh

exec \
  "$(dirname "$0")/run_python_script_in_container.sh" \
  "type_python" \
  "$@"
