from __future__ import annotations

import dataclasses
import os
import pathlib
import platform
import re
import subprocess
from absl.testing import absltest


CMAKE_MODULE_PATH = pathlib.Path(__file__).parent / "GetUserHomeDir.cmake"


class GetUserHomeDirTest(absltest.TestCase):

  def test_fails_when_given_an_extra_argument(self):
    result = self.callGetUserHomeDir(extra_arguments=["zzyzx"])
    self.assertNotEqual(
        result.exit_code,
        0,
        "GetUserHomeDir() should have failed, "
        f"but it completed successfully with result: {result.return_value}",
    )
    self.assertIn(
        "GetUserHomeDir was invoked with 2 arguments, "
        "but exactly 1 expected (unexpected arguments: zzyzx)",
        result.output,
    )

  def test_returns_not_found_if_home_and_userprofile_env_vars_not_set(self):
    self.assertGetUserHomeDirReturns("NOTFOUND", env_unset=["HOME", "USERPROFILE"])

  @absltest.skipUnless(platform.system() == "Windows", "USRPROFILE is only used on Windows")
  def test_returns_userprofile_env_var_if_set_on_windows(self):
    self.assertGetUserHomeDirReturns("abcdef", env={"USERPROFILE": "abcdef"})

  @absltest.skipIf(platform.system() == "Windows", "USRPROFILE *is* used on Windows")
  def test_ignores_userprofile_env_var_if_set_on_non_windows(self):
    self.assertGetUserHomeDirReturns("NOTFOUND", env={"USERPROFILE": "abcdef"}, env_unset=["HOME"])

  @absltest.skipIf(platform.system() == "Windows", "HOME is only used on non-Windows")
  def test_returns_home_env_var_if_set_on_non_windows(self):
    self.assertGetUserHomeDirReturns("abcdef", env={"HOME": "abcdef"})

  @absltest.skipUnless(platform.system() == "Windows", "HOME *is* used on non-Windows")
  def test_ignores_home_env_var_if_set_on_windows(self):
    self.assertGetUserHomeDirReturns("NOTFOUND", env={"HOME": "abcdef"}, env_unset=["USERPROFILE"])

  def assertGetUserHomeDirReturns(
      self,
      expected_result: str,
      env: dict[str, str] | None = None,
      env_unset: list[str] | None = None,
  ) -> str:
    result = self.callGetUserHomeDir(env=env, env_unset=env_unset)
    self.assertEqual(
        result.exit_code,
        0,
        "GetUserHomeDir() failed, "
        "but should have completed successfully with result: {expected_result} "
        f"(output: {result.output})",
    )
    self.assertEqual(result.return_value, expected_result)

  def callGetUserHomeDir(
      self,
      extra_arguments: list[str] | None = None,
      env: dict[str, str] | None = None,
      env_unset: list[str] | None = None,
  ) -> GetUserHomeDirResult:
    extra_arguments_str = " ".join(extra_arguments) if extra_arguments is not None else ""

    subprocess_env = dict(os.environ)
    if env_unset is not None:
      for env_var_to_unset in env_unset:
        if env_var_to_unset in subprocess_env:
          del subprocess_env[env_var_to_unset]
    if env is not None:
      subprocess_env.update(env)

    function_result_file = pathlib.Path(self.create_tempfile())
    cmake_text = f"""
      include("{CMAKE_MODULE_PATH.as_posix()}")
      GetUserHomeDir(FUNCTION_RESULT {extra_arguments_str})
      file(WRITE "{function_result_file.as_posix()}" "${{FUNCTION_RESULT}}")
    """
    cmake_script_path = self.create_tempfile(content=cmake_text)
    process = subprocess.run(
        ["cmake", "-P", cmake_script_path],
        env=subprocess_env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        encoding="utf8",
        errors="replace",
    )

    function_result = function_result_file.read_text(encoding="utf8", errors="replace")
    return self.GetUserHomeDirResult(
        exit_code=process.returncode,
        return_value=function_result,
        output=re.sub(r"\s+", " ", process.stdout),
    )

  @dataclasses.dataclass(frozen=True)
  class GetUserHomeDirResult:
    exit_code: int
    return_value: str
    output: str


if __name__ == "__main__":
  absltest.main()
