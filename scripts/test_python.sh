#!/bin/sh

readonly workdir="$(readlink -f "$(dirname "$0")")/.."

exec \
  podman \
  run \
  --rm \
  --mount "type=bind,src=$workdir,dst=$workdir" \
  --workdir "$workdir" \
  docker.io/lakeoak/conccpp_python:2 \
  python -m scripts.test_python \
  "$@"

