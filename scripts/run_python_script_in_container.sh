#!/bin/sh

readonly workdir="$(readlink -f "$(dirname "$0")")/.."
readonly script_name="$1"
shift

exec \
  podman \
  run \
  --rm \
  --mount "type=bind,src=$workdir,dst=$workdir" \
  --workdir "$workdir" \
  docker.io/lakeoak/conccpp_python:2 \
  python -m "scripts.$script_name" \
  "$@"
