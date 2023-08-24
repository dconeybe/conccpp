from __future__ import annotations

import dataclasses
import os
import pathlib
import re
import subprocess

from absl.testing import absltest


def call_cmake_function(
    test_case: absltest.TestCase,
    cmake_file: pathlib.Path,
    function_name: str,
    function_out_var: str,
    function_arguments: list[str] | None = None,
    env: dict[str, str] | None = None,
    env_unset: list[str] | None = None,
) -> CmakeFunctionResult:
  function_arguments_str = " ".join(function_arguments) if function_arguments is not None else ""

  subprocess_env = dict(os.environ)
  if env_unset is not None:
    for env_var_to_unset in env_unset:
      if env_var_to_unset in subprocess_env:
        del subprocess_env[env_var_to_unset]
  if env is not None:
    subprocess_env.update(env)

  function_result_file = pathlib.Path(test_case.create_tempfile())

  cmake_text = f"""
    include("{cmake_file.as_posix()}")
    {function_name}({function_arguments_str})
    file(WRITE "{function_result_file.as_posix()}" "${{{function_out_var}}}")
  """
  cmake_script_path = test_case.create_tempfile(content=cmake_text)
  process = subprocess.run(
      ["cmake", "-P", cmake_script_path],
      env=subprocess_env,
      stdout=subprocess.PIPE,
      stderr=subprocess.STDOUT,
      encoding="utf8",
      errors="replace",
  )

  if process.returncode == 0:
    function_return_value = function_result_file.read_text(encoding="utf8", errors="replace")
  else:
    function_return_value = None

  return CmakeFunctionResult(
      return_value=function_return_value,
      output=re.sub(r"\s+", " ", process.stdout),
  )


@dataclasses.dataclass(frozen=True)
class CmakeFunctionResult:
  return_value: str | None
  output: str
