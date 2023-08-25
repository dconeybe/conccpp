from __future__ import annotations

import collections
import pathlib

from absl.testing import absltest

import util


CMAKE_MODULE_PATH = pathlib.Path(__file__).parent.parent / "ConcppGetValueForCompiler.cmake"


class ConcppGetValueForCompilerTest(absltest.TestCase):

  def test_returns_gcc_value_when_compiler_frontend_is_GNU(self):
    self.assertConcppGetValueForCompilerReturns(
        expected_result="zzyzx_gcc",
        gcc_value="zzyzx_gcc",
        msvc_value="zzyzx_msvc",
        default_value="zzyzx_default",
        compiler_frontend_variant="GNU",
    )

  def test_returns_gcc_value_when_compiler_id_is_GNU(self):
    self.assertConcppGetValueForCompilerReturns(
        expected_result="zzyzx_gcc",
        gcc_value="zzyzx_gcc",
        msvc_value="zzyzx_msvc",
        default_value="zzyzx_default",
        compiler_id="GNU",
    )

  def test_returns_gcc_value_when_compiler_frontend_is_Clang(self):
    self.assertConcppGetValueForCompilerReturns(
        expected_result="zzyzx_gcc",
        gcc_value="zzyzx_gcc",
        msvc_value="zzyzx_msvc",
        default_value="zzyzx_default",
        compiler_frontend_variant="Clang",
    )

  def test_returns_gcc_value_when_compiler_id_is_Clang(self):
    self.assertConcppGetValueForCompilerReturns(
        expected_result="zzyzx_gcc",
        gcc_value="zzyzx_gcc",
        msvc_value="zzyzx_msvc",
        default_value="zzyzx_default",
        compiler_id="Clang",
    )

  def test_returns_gcc_value_when_compiler_frontend_is_AppleClang(self):
    self.assertConcppGetValueForCompilerReturns(
        expected_result="zzyzx_gcc",
        gcc_value="zzyzx_gcc",
        msvc_value="zzyzx_msvc",
        default_value="zzyzx_default",
        compiler_frontend_variant="AppleClang",
    )

  def test_returns_gcc_value_when_compiler_id_is_AppleClang(self):
    self.assertConcppGetValueForCompilerReturns(
        expected_result="zzyzx_gcc",
        gcc_value="zzyzx_gcc",
        msvc_value="zzyzx_msvc",
        default_value="zzyzx_default",
        compiler_id="AppleClang",
    )

  def test_returns_msvc_value_when_compiler_frontend_is_MSVC(self):
    self.assertConcppGetValueForCompilerReturns(
        expected_result="zzyzx_msvc",
        gcc_value="zzyzx_gcc",
        msvc_value="zzyzx_msvc",
        default_value="zzyzx_default",
        compiler_frontend_variant="MSVC",
    )

  def test_returns_msvc_value_when_compiler_id_is_MSVC(self):
    self.assertConcppGetValueForCompilerReturns(
        expected_result="zzyzx_msvc",
        gcc_value="zzyzx_gcc",
        msvc_value="zzyzx_msvc",
        default_value="zzyzx_default",
        compiler_id="MSVC",
    )

  def test_returns_default_value_when_compiler_frontend_is_something_else(self):
    self.assertConcppGetValueForCompilerReturns(
        expected_result="zzyzx_default",
        gcc_value="zzyzx_gcc",
        msvc_value="zzyzx_msvc",
        default_value="zzyzx_default",
        compiler_frontend_variant="SomethingElse",
    )

  def test_returns_default_value_when_compiler_id_is_something_else(self):
    self.assertConcppGetValueForCompilerReturns(
        expected_result="zzyzx_default",
        gcc_value="zzyzx_gcc",
        msvc_value="zzyzx_msvc",
        default_value="zzyzx_default",
        compiler_id="SomethingElse",
    )

  def test_compiler_frontent_variant_takes_precendence_over_compiler_id_GNU(self):
    self.assertConcppGetValueForCompilerReturns(
        expected_result="zzyzx_gcc",
        gcc_value="zzyzx_gcc",
        msvc_value="zzyzx_msvc",
        default_value="zzyzx_default",
        compiler_frontend_variant="GNU",
        compiler_id="MSVC",
    )

  def test_compiler_frontent_variant_takes_precendence_over_compiler_id_MSVC(self):
    self.assertConcppGetValueForCompilerReturns(
        expected_result="zzyzx_msvc",
        gcc_value="zzyzx_gcc",
        msvc_value="zzyzx_msvc",
        default_value="zzyzx_default",
        compiler_frontend_variant="MSVC",
        compiler_id="GNU",
    )

  def assertConcppGetValueForCompilerReturns(
      self,
      expected_result: str,
      gcc_value: str,
      msvc_value: str,
      default_value: str,
      compiler_frontend_variant: str | None = None,
      compiler_id: str | None = None,
  ) -> None:
    result = self.callConcppGetValueForCompiler(
        gcc_value=gcc_value,
        msvc_value=msvc_value,
        default_value=default_value,
        compiler_frontend_variant=compiler_frontend_variant,
        compiler_id=compiler_id,
    )

    self.assertIsNotNone(
        result.return_value,
        "ConcppGetValueForCompiler() failed, "
        "but should have completed successfully with result: {expected_result} "
        f"output: {result.output} "
        f"cmake script: {result.script}",
    )
    self.assertEqual(
        result.return_value,
        expected_result,
        "ConcppGetValueForCompiler() returned a different value from what was expected; "
        f"output: {result.output} "
        f"cmake script: {result.script}",
    )

  def callConcppGetValueForCompiler(
      self,
      gcc_value: str,
      msvc_value: str,
      default_value: str,
      compiler_frontend_variant: str | None = None,
      compiler_id: str | None = None,
      extra_arguments: list[str] | None = None,
  ) -> util.CmakeFunctionResult:
    function_arguments = ["return_value", gcc_value, msvc_value, default_value]
    if extra_arguments is not None:
      function_arguments.extend(extra_arguments)

    cmake_variables: collections.OrderedDict[str, str] = collections.OrderedDict()
    if compiler_frontend_variant is not None:
      cmake_variables["CMAKE_CXX_COMPILER_FRONTEND_VARIANT"] = compiler_frontend_variant
    if compiler_id is not None:
      cmake_variables["CMAKE_CXX_COMPILER_ID"] = compiler_id

    return util.call_cmake_function(
        test_case=self,
        cmake_file=CMAKE_MODULE_PATH,
        function_name="ConcppGetValueForCompiler",
        function_out_var="return_value",
        function_arguments=function_arguments,
        cmake_variables=cmake_variables,
    )


if __name__ == "__main__":
  absltest.main()
