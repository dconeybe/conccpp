#!/bin/sh

set -x
exec podman run --rm --mount "type=bind,src=$PWD,dst=/src" docker.io/lakeoak/conccpp_python:1 python scripts/pyformat.py "$@"
