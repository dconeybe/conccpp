#!/bin/sh

set -v
exec podman run --rm -v $PWD:/src concpp_python python scripts/pyformat.py "$@"
