import dataclasses
import enum
import pathlib

from absl import app
from absl import flags
import jinja2

def main(argv: list[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError(f"unexpected argument: {argv[1]}")

  template_dir = pathlib.Path(__file__).parent

  env = jinja2.Environment(
      variable_start_string="{$",
      variable_end_string="$}",
      autoescape=False,
      loader=jinja2.FileSystemLoader(template_dir),
  )

  template = env.get_template("index.txt")

  rendered_template = template.render(cpp_tests=cpp_tests())

  print(rendered_template)


@dataclasses.dataclass(frozen=True)
class CppTestParameters:
  os_name: str
  github_runs_on: str
  build_config: str
  compiler: str | None = None
  target_architecture: str | None = None


def cpp_tests() -> list[CppTestParameters]:
  return [
    CppTestParameters(
      os_name="linux",
      github_runs_on="ubuntu-latest",
      build_config="Debug",
      compiler="gcc",
    ),
    CppTestParameters(
      os_name="linux",
      github_runs_on="ubuntu-latest",
      build_config="Release",
      compiler="gcc",
    ),
    CppTestParameters(
      os_name="linux",
      github_runs_on="ubuntu-latest",
      build_config="Debug",
      compiler="clang",
    ),
    CppTestParameters(
      os_name="linux",
      github_runs_on="ubuntu-latest",
      build_config="Release",
      compiler="clang",
    ),
    CppTestParameters(
      os_name="macos",
      github_runs_on="macos-latest",
      build_config="Debug",
    ),
    CppTestParameters(
      os_name="macos",
      github_runs_on="macos-latest",
      build_config="Release",
    ),
    CppTestParameters(
      os_name="windows",
      github_runs_on="windows-latest",
      build_config="Debug",
      target_architecture="Win32",
    ),
    CppTestParameters(
      os_name="windows",
      github_runs_on="windows-latest",
      build_config="Release",
      target_architecture="Win32",
    ),
    CppTestParameters(
      os_name="windows",
      github_runs_on="windows-latest",
      build_config="Debug",
      target_architecture="x64",
    ),
    CppTestParameters(
      os_name="windows",
      github_runs_on="windows-latest",
      build_config="Release",
      target_architecture="x64",
    ),
  ]


if __name__ == "__main__":
  app.run(main)
