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

  rendered_template = template.render(
      BuildConfig=BuildConfig,
      Compiler=Compiler,
      CppTestParameters=CppTestParameters,
      OperatingSystem=OperatingSystem,
  )

  print(rendered_template)


@enum.unique
class OperatingSystem(enum.Enum):
  LINUX = enum.auto()
  MACOS = enum.auto()
  WINDOWS = enum.auto()


@enum.unique
class BuildConfig(enum.Enum):
  RELEASE = enum.auto()
  DEBUG = enum.auto()


@enum.unique
class Compiler(enum.Enum):
  GCC = enum.auto()
  CLANG = enum.auto()


@dataclasses.dataclass(frozen=True)
class CppTestParameters:
  operating_system: OperatingSystem
  build_config: BuildConfig
  compiler: Compiler | None = None
  target_architecture: str | None = None


if __name__ == "__main__":
  app.run(main)
