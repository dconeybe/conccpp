"""
Run the Python unit tests.

Syntax: %s [flags]
"""

from collections.abc import Sequence
import subprocess
import sys

from absl import app
from absl import logging

from . import source_file_finder


def main(args: Sequence[str]) -> None:
  if len(args) > 1:
    print(f"ERROR: unexpected argument: {args[1]}", file=sys.stderr)
    return 2

  paths = source_file_finder.find_sources("*.test.py")
  path_strs = [str(path) for path in paths]

  pass_count = 0
  fail_count = 0
  for path_str in sorted(path_strs):
    args = [sys.executable, path_str]
    logging.debug(subprocess.list2cmdline(args))
    completed_process = subprocess.run(args)
    if completed_process.returncode == 0:
      pass_count += 1
    else:
      fail_count += 1

  print_test_summary(pass_count=pass_count, fail_count=fail_count)
  return 0 if fail_count == 0 else 1


def print_test_summary(pass_count: int, fail_count: int) -> None:
  if fail_count == 0:
    print(f"All {pass_count} tests passed :)")
    return

  print(f"Tests Run:    {pass_count+fail_count}")
  print(f"Tests Passed: {pass_count}")
  print(f"Tests Failed: {fail_count}")
  print()
  print("***************************************************************")
  print("** TEST FAILURES OCCURRED")
  print("***************************************************************")


if __name__ == "__main__":
  app.run(main)
