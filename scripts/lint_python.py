"""
Run the Python linter on all Python source files.

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

  pyflakes_args = ["pyflakes"]
  pyflakes_args.extend(str(path) for path in paths)

  logging.debug(subprocess.list2cmdline(pyflakes_args))
  completed_process = subprocess.run(pyflakes_args)
  return completed_process.returncode


if __name__ == "__main__":
  app.run(main)
