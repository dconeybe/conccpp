#!/bin/sh

set -x

exec \
  podman \
  run \
  --rm \
  --mount "type=bind,src=$PWD,dst=$PWD" \
  --workdir "$PWD" \
  docker.io/lakeoak/conccpp_python:2 \
  python -m scripts.pyformat \
  "$@"
