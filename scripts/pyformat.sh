#!/bin/sh

set -x
exec podman run --rm --mount "type=bind,src=$PWD,dst=/src" concpp_python python scripts/pyformat.py "$@"
