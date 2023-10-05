"""
Check Python types with pytype.

Syntax: %s [flags]
"""

from collections.abc import Sequence
import subprocess
import sys

from absl import app
from absl import logging

from . import source_file_finder


def main(args: Sequence[str]) -> int:
  if len(args) > 1:
    print(f"ERROR: unexpected argument: {args[1]}", file=sys.stderr)
    return 2
  del args

  paths = source_file_finder.find_sources("*.py")

  pytype_args = [
      "pytype",
      "--keep-going",
      "--python-version=3.10",
      "--no-cache",
      "--overriding-parameter-count-checks",
      "--overriding-renamed-parameter-count-checks",
      "--use-enum-overlay",
      "--strict-none-binding",
      "--strict-parameter-checks",
      "--strict-primitive-comparisons",
      "--strict-undefined-checks",
  ]

  pytype_args.extend(str(path) for path in paths)

  logging.debug(subprocess.list2cmdline(pytype_args))
  completed_process = subprocess.run(pytype_args)
  return completed_process.returncode


if __name__ == "__main__":
  app.run(main)
