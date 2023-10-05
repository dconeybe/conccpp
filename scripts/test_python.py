"""
Run the Python unit tests.

Syntax: %s [flags]
"""

from collections.abc import Sequence
import dataclasses
import pathlib
import subprocess
import sys
import tempfile
import xml.dom.minidom as minidom

from absl import app
from absl import logging

from . import source_file_finder


def main(args: Sequence[str]) -> None:
  if len(args) > 1:
    print(f"ERROR: unexpected argument: {args[1]}", file=sys.stderr)
    return 2
  del args

  paths = source_file_finder.find_sources("*.test.py")
  path_strs = [str(path) for path in paths]

  pass_count = 0
  fail_count = 0
  error_count = 0
  next_xml_results_file_number = 1

  with tempfile.TemporaryDirectory() as temp_dir_path:
    temp_dir = pathlib.Path(temp_dir_path)
    del temp_dir_path

    for path_str in sorted(path_strs):
      xml_results_file = temp_dir / f"test_results_{next_xml_results_file_number:05}.xml"
      next_xml_results_file_number += 1

      test_args = [sys.executable, path_str, f"--xml_output_file={xml_results_file}"]
      logging.info(subprocess.list2cmdline(test_args))
      subprocess.run(test_args)

      if not xml_results_file.is_file():
        error_count += 1
        continue

      test_results = parse_xml_result_file(xml_results_file)
      xml_results_file.unlink()
      pass_count += test_results.pass_count
      fail_count += test_results.fail_count
      error_count += test_results.error_count

  print_test_summary(pass_count, fail_count, error_count)
  return 0 if fail_count == 0 and error_count == 0 else 1


@dataclasses.dataclass(frozen=True)
class TestResults:
  pass_count: int
  fail_count: int
  error_count: int


def parse_xml_result_file(path: pathlib.Path) -> TestResults:
  logging.debug("Loading test results from file: %s", path)
  xml_document = minidom.parse(str(path))

  expected_document_element_name = "testsuites"
  if xml_document.documentElement.nodeName != expected_document_element_name:
    raise XmlResultsFileParseError(
        f"unexpected document element name in {path}: "
        f"{xml_document.documentElement.nodeName} (expected {expected_document_element_name})"
    )

  attributes = xml_document.documentElement.attributes
  test_count = int(attributes["tests"].value)
  fail_count = int(attributes["failures"].value)
  error_count = int(attributes["errors"].value)

  test_results = TestResults(
      pass_count=test_count - fail_count - error_count,
      fail_count=fail_count,
      error_count=error_count,
  )
  logging.debug("Loaded test results from %s: %s", path, test_results)
  return test_results


class XmlResultsFileParseError(Exception):
  pass


def print_test_summary(pass_count: int, fail_count: int, error_count: int) -> None:
  print()

  if fail_count == 0 and error_count == 0:
    print(f"All {pass_count} tests passed :)")
    return

  print("***************************************************************")
  print()
  print(f"Tests Run:    {pass_count+fail_count}")
  print(f"Tests Passed: {pass_count}")
  print(f"Tests Failed: {fail_count}")
  print(f"Test Errors:  {error_count}")
  print()
  print("***************************************************************")
  print("** TEST FAILURES AND/OR ERRORS OCCURRED")
  print("***************************************************************")


if __name__ == "__main__":
  app.run(main)
