import dataclasses
import pathlib
import re

from absl import app
import jinja2
import jinja2.ext
import jinja2.exceptions


def main(argv: list[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError(f"unexpected argument: {argv[1]}")

  template_dir = pathlib.Path(__file__).parent

  env = jinja2.Environment(
      variable_start_string="{$",
      variable_end_string="$}",
      autoescape=False,
      lstrip_blocks=True,
      trim_blocks=True,
      loader=jinja2.FileSystemLoader(template_dir),
      undefined=jinja2.StrictUndefined,
      extensions=[RaiseExtension],
  )
  env.filters["replace_whitespace_with"] = replace_whitespace_with

  template = env.get_template("index.txt")

  rendered_template = template.render(
    CppTestParams=CppTestParams,
  )

  print(rendered_template)


def replace_whitespace_with(value: str, replacement: str) -> str:
  return re.sub(r"\s+", replacement, value, flags=re.DOTALL)


# Adapted from https://github.com/duelafn/python-jinja2-apci/blob/master/jinja2_apci/error.py
class RaiseExtension(jinja2.ext.Extension):
  """
  A Jinja2 extension that adds a "raise" tag to the language, which takes a single string argument
  and raises an exception.

  e.g. {% raise "Should never get here" %}
  """

  tags = set(["raise"])

  def parse(self, parser):
    # the first token is the token that started the tag. In our case we
    # only listen to "raise" so this will be a name token with
    # "raise" as value. We get the line number so that we can give
    # that line number to the nodes we insert.
    lineno = next(parser.stream).lineno

    # Extract the message from the template
    message_node = parser.parse_expression()

    return jinja2.nodes.CallBlock(
        self.call_method("_raise", [message_node], lineno=lineno), [], [], [], lineno=lineno
    )

  def _raise(self, msg, caller):
    raise jinja2.exceptions.TemplateRuntimeError(msg)


@dataclasses.dataclass(frozen=True)
class CppTestParams:
  operating_system: str
  build_config: str
  compiler: tuple[str, str] | None = None
  sanitizer: str | None = None
  target_architecture: str | None = None


if __name__ == "__main__":
  app.run(main)
