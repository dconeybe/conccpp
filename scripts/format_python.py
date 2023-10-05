"""
Run the Python code style formatter on all Python source files.

Syntax: %s [flags]
"""

from collections.abc import Sequence
import subprocess
import sys

from absl import app
from absl import flags
from absl import logging

from . import source_file_finder


FLAG_CHECK_ONLY = flags.DEFINE_boolean(
    "check",
    False,
    "If this flag is true then just check the files for formatting errors, but do not modify them. "
    "If this flag is false then modify the files in-place to fix formatting errors. "
    "If this flag is true, then the exit code of this application will be zero if no formatting "
    "errors were found, or non-zero if one or more formatting errors were found.",
)


def main(args: Sequence[str]) -> None:
  if len(args) > 1:
    print(f"ERROR: unexpected argument: {args[1]}", file=sys.stderr)
    return 2
  del args

  paths = source_file_finder.find_sources("*.py")

  pyink_args = [
      "pyink",
      "--line-length=100",
      "--target-version=py311",
      "--pyink",
      "--pyink-indentation=2",
  ]

  if FLAG_CHECK_ONLY.value:
    pyink_args.extend([
        "--check",
        "--diff",
    ])

  pyink_args.extend(str(path) for path in paths)

  logging.debug(subprocess.list2cmdline(pyink_args))
  completed_process = subprocess.run(pyink_args)
  return completed_process.returncode


if __name__ == "__main__":
  app.run(main)
