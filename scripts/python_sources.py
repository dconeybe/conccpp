import pathlib
import subprocess
import tempfile


def find_python_sources() -> list[pathlib.Path]:
  cwd = pathlib.Path.cwd()
  expected_cwd = pathlib.Path(__file__).parent.parent
  if not cwd.samefile(expected_cwd):
    raise UnexpectedCurrentDirectory(f"current directory is {cwd}, but expected {expected_cwd}")

  paths = [path.relative_to(cwd) for path in cwd.glob("**/*.py") if path.is_file()]
  path_strings = [str(path) for path in paths]

  args = ["git", "check-ignore"]
  args.extend(path_strings)

  with tempfile.TemporaryFile() as output_file:
    completed_process = subprocess.run(args, stdout=output_file)

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

  output_text = output.decode("utf8", errors="ignore")
  ignored_path_strings = frozenset(line.strip() for line in output_text.splitlines())

  unignored_files: list[pathlib.Path] = []
  for i in range(len(paths)):
    path_string = path_strings[i]
    if path_string not in ignored_path_strings:
      unignored_files.append(paths[i])

  return unignored_files


class UnexpectedCurrentDirectory(Exception):
  pass
