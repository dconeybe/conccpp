#!/bin/bash

set -euo pipefail
set -xv

exec podman build -f scripts/python.dockerfile -t concpp_python
