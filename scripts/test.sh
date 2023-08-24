#!/bin/bash

set -euo pipefail

pass_count=0
fail_count=0

for f in cmake/*.test.py ; do
  echo "Running test: $f"
  if python "$f" ; then
    pass_count=$((pass_count + 1))
  else
    fail_count=$((fail_count + 1))
  fi
done

echo
echo '------------'
echo 'TEST SUMMARY'
echo '------------'
echo "Tests Run:    $((pass_count+fail_count))"
echo "Tests Passed: ${pass_count}"
echo "Tests Failed: ${fail_count}"

if [[ fail_count -gt 0 ]] ; then
  echo
  echo '***************************************************************'
  echo '** TEST FAILURES OCCURRED'
  echo '***************************************************************'
  exit 1
fi
