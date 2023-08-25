#!/bin/bash

set -euo pipefail

pass_count=0
fail_count=0

for f in cmake/test/*.test.py ; do
  echo "Running test: $f"
  if python "$f" ; then
    pass_count=$((pass_count + 1))
  else
    fail_count=$((fail_count + 1))
  fi
done

echo
if [[ fail_count -eq 0 ]] ; then
  echo "All ${pass_count} tests passed :)"
else
  echo "Tests Run:    $((pass_count+fail_count))"
  echo "Tests Passed: ${pass_count}"
  echo "Tests Failed: ${fail_count}"
  echo
  echo '***************************************************************'
  echo '** TEST FAILURES OCCURRED'
  echo '***************************************************************'
  exit 1
fi
