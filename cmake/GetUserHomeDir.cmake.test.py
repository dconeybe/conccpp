from __future__ import annotations

import pathlib
import platform

from absl.testing import absltest

import util


CMAKE_MODULE_PATH = pathlib.Path(__file__).parent / "GetUserHomeDir.cmake"


class GetUserHomeDirTest(absltest.TestCase):

  def test_fails_when_given_an_extra_argument(self):
    result = self.callGetUserHomeDir(extra_arguments=["zzyzx"])
    self.assertIsNone(
        result.return_value,
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
    self.assertIsNotNone(
        result.return_value,
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
  ) -> util.CmakeFunctionResult:
    function_arguments = ["GET_USER_HOME_DIR_RESULT"]
    if extra_arguments is not None:
      function_arguments.extend(extra_arguments)
    return util.call_cmake_function(
        test_case=self,
        cmake_file=CMAKE_MODULE_PATH,
        function_name="GetUserHomeDir",
        function_out_var="GET_USER_HOME_DIR_RESULT",
        function_arguments=function_arguments,
        env=env,
        env_unset=env_unset,
    )


if __name__ == "__main__":
  absltest.main()
