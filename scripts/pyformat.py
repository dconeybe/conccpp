"""
Run the Python code style formatter on all Python source files.

Syntax: %s [flags]
"""

from collections.abc import Sequence
import pathlib
import subprocess
import sys
import tempfile

from absl import app
from absl import flags
from absl import logging


FLAG_CHECK_ONLY = flags.DEFINE_boolean(
    "check",
    False,
    "If this flag is true then just check the files for formatting errors, but do not modify them. "
    "If this flag is false then modify the files in-place to fix formatting errors. "
    "If this flag is true, then the exit code of this application will be zero if no formatting "
    "errors were found, or non-zero if one or more formatting errors were found.",
)


def main(args: Sequence[str]) -> None:
  cwd = pathlib.Path.cwd()
  paths = [path.relative_to(cwd) for path in cwd.glob("**/*.py") if path.is_file()]
  paths = git_ignored_files_removed(paths)

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

  print(subprocess.list2cmdline(pyink_args))
  completed_process = subprocess.run(pyink_args)
  return completed_process.returncode


def git_ignored_files_removed(paths: Sequence[pathlib.Path]) -> list[pathlib.Path]:
  def path_str_from_path(path: pathlib.Path) -> str:
    cwd = pathlib.Path.cwd()
    resolved_path = path.resolve(strict=False)
    path_string1 = str(resolved_path)
    path_string2 = str(resolved_path.relative_to(cwd))
    return path_string1 if len(path_string1) <= len(path_string2) else path_string2

  path_strings = [path_str_from_path(path) for path in paths]

  args = ["git", "check-ignore"]
  args.extend(path_strings)

  with tempfile.TemporaryFile() as output_file:
    completed_process = subprocess.run(args)

    match exit_code := completed_process.returncode:
      case 1:
        # Note: `git check-ignore` completes with an exit code of 1 when _none_ of the given files
        # were ignored.
        return paths
      case 0:
        output_file.seek(0)
        output = output_file.read()
      case _:
        raise Exception(f"git check-ignore failed with non-zero exit code: {exit_code}")

  lines = output.decode("utf8", errors="ignore").splitlines()
  ignored_path_strings = frozenset(line.strip() for line in lines)

  unignored_files: list[pathlib.Path] = []
  for i in range(len(paths)):
    path_string = path_strings[i]
    if path_string not in ignored_path_strings:
      unignored_files.append(paths[i])

  return unignored_files


if __name__ == "__main__":
  app.run(main)
