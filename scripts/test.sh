#!/bin/bash

set -euo pipefail

for f in cmake/*.py ; do
  echo "Running test: $f"
  python "$f"
done
