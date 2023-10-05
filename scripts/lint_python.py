"""
Run the Python linter on all Python source files.

Syntax: %s [flags]
"""

from collections.abc import Sequence
import subprocess
import sys

from absl import app
from absl import logging

from . import python_sources


def main(args: Sequence[str]) -> None:
  if len(args) > 1:
    print(f"ERROR: unexpected argument: {args[1]}", file=sys.stderr)
    return 2

  paths = python_sources.find_python_sources()

  pyflakes_args = ["pyflakes"]
  pyflakes_args.extend(str(path) for path in paths)

  logging.debug(subprocess.list2cmdline(pyflakes_args))
  completed_process = subprocess.run(pyflakes_args)
  return completed_process.returncode


if __name__ == "__main__":
  app.run(main)
