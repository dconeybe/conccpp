from __future__ import annotations

from collections.abc import Iterable, Mapping
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
    function_arguments: Iterable[str] | None = None,
    env: Mapping[str, str] | None = None,
    env_unset: Iterable[str] | None = None,
    cmake_variables: Mapping[str, str] | None = None,
) -> CmakeFunctionResult:
  subprocess_env = dict(os.environ)
  if env_unset is not None:
    for env_var_to_unset in env_unset:
      if env_var_to_unset in subprocess_env:
        del subprocess_env[env_var_to_unset]
  if env is not None:
    subprocess_env.update(env)

  function_result_file = pathlib.Path(test_case.create_tempfile())
  cmake_text = os.linesep.join(
      _cmake_text(
          cmake_file=cmake_file,
          function_name=function_name,
          function_arguments=function_arguments,
          function_result_file=function_result_file,
          function_out_var=function_out_var,
          cmake_variables=cmake_variables,
      )
  )

  cmake_script_path = test_case.create_tempfile(content=cmake_text)
  process = subprocess.run(
      ["cmake", "-P", cmake_script_path, "--log-level=VERBOSE", "--log-context"],
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
      output=process.stdout,
      output_singleline=re.sub(r"\s+", " ", process.stdout),
      script=cmake_text,
  )


@dataclasses.dataclass(frozen=True)
class CmakeFunctionResult:
  return_value: str | None
  output: str
  output_singleline: str
  script: str


def _cmake_text(
    cmake_file: pathlib.Path,
    function_name: str,
    function_arguments: Iterable[str] | None,
    function_result_file: pathlib.Path,
    function_out_var: str,
    cmake_variables: Mapping[str, str] | None,
) -> Iterable[str]:
  function_arguments_str = " ".join(function_arguments) if function_arguments is not None else ""
  yield f"""include("{cmake_file.as_posix()}")"""
  if cmake_variables is not None:
    for cmake_variable_name, cmake_variable_value in cmake_variables.items():
      yield f"""set({cmake_variable_name} "{cmake_variable_value}")"""
  yield f"""{function_name}({function_arguments_str})"""
  yield f"""file(WRITE "{function_result_file.as_posix()}" "${{{function_out_var}}}")"""
