import pathlib

from absl import app
from absl import flags
import jinja2

def main(argv: list[str]) -> None:
  if len(argv) > 1:
    raise app.UsageError(f"unexpected argument: {argv[1]}")

  template_dir = pathlib.Path(__file__).parent

  env = jinja2.Environment(
      variable_start_string="{@",
      variable_end_string="@}",
      autoescape=False,
      loader=jinja2.FileSystemLoader(template_dir),
  )

  template = env.get_template("index.txt")

  rendered_template = template.render()

  print(rendered_template)


if __name__ == "__main__":
  app.run(main)
