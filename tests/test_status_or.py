# Copyright 2025 by Martin Urban.
#
# It is unlawful to modify or remove this copyright notice.
# Licensed under the BSD-3-Clause;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://opensource.org/license/bsd-3-clause
#
# or please see the accompanying LICENSE file for further information.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
---------------------------------------------------------------------------
File: tests/test_status_or.py
---------------------------------------------------------------------------

This file defines a number of tests to verify the functionality of the
StatusOr class.
"""

import pathlib

import kern_comm_lib as kern


def add_to_list(src_list: list, new_item: int) -> kern.Status:
  """Add two numbers."""
  if len(src_list) == 0:
    return kern.status.invalid_argument_error("List is empty!")
  src_list.append(new_item)
  return kern.Status()


def divide(a: int, b: int) -> kern.AStatusOrElse[float]:
  """Divide two numbers."""
  if b == 0:
    return kern.status.zero_division_error("Division by zero!")
  return a / b


@kern.use_status
def exists(path: pathlib.Path) -> kern.AStatusOrElse[bool]:
  """Checks if a path exists but in an exception-free way."""
  return path.exists()


def test_decorator() -> None:
  """Tests the decorator."""
  tmp_path = pathlib.Path("test.txt")
  tmp_status = kern.StatusOr(bool, exists(tmp_path))
  if tmp_status.ok():
    print(f"Path exists: {tmp_path}")
  else:
    print(f"Error: {tmp_status.status()}")


def test_status_or_init() -> None:
  """Tests the initialization of StatusOr class."""
  tmp_list = [1, 2, 3]
  tmp_status: kern.Status = add_to_list(tmp_list, 4)
  assert tmp_status.ok() is True

  tmp_list = []
  tmp_status = add_to_list(tmp_list, 4)
  assert tmp_status.ok() is False

  tmp_number = kern.StatusOr(float, divide(1, 0))
  if tmp_number.ok():
    print(tmp_number.val())
  else:
    print(tmp_number.status())


def test_experiment() -> None:
  """Tests to experiment."""
  try:
    pathlib.Path("test.txt").open()  # noqa: SIM115
  except Exception as e:
    print(f"Error: {e}")
    kern.Status.from_exception(e)


def test_status_or_contains_value() -> None:
  """Tests that StatusOr correctly handles and returns a valid value.

  Verifies that a StatusOr initialized with a valid integer value:
  1. Reports ok() as True
  2. Returns the correct value via val()
  """
  tmp_val = 42
  result = kern.StatusOr(int, tmp_val)
  assert result.ok() is True
  assert result.val() == tmp_val


def test_status_or_contains_error() -> None:
  """Tests that StatusOr correctly handles an error status.

  Verifies that a StatusOr initialized with an error status:
  1. Reports ok() as False
  2. Returns the same error status via status()
  """
  error_status = kern.status.invalid_argument_error("Invalid argument")
  result = kern.StatusOr(int, error_status)
  assert result.ok() is False
  assert result.status() == error_status


def test_status_or_type_mismatch() -> None:
  """Tests that StatusOr rejects type mismatches.

  Verifies that initializing a StatusOr with a value of incorrect type
  (string instead of int) raises a SystemExit exception.
  """
  try:
    kern.StatusOr(int, "string")
  except SystemExit:
    assert True
  else:
    assert False


def test_status_or_ok_status() -> None:
  """Tests that StatusOr with a valid value has OK status code.

  Verifies that a StatusOr initialized with a valid value
  has a status with StatusCode.OK.
  """
  result = kern.StatusOr(int, 42)
  assert result.status().status_code() == kern.StatusCode.OK


def test_status_or_none_value() -> None:
  """Tests that StatusOr correctly handles None values.

  Verifies that a StatusOr initialized with None:
  1. Reports ok() as True
  2. Returns None via val()
  """
  result = kern.StatusOr(int, None)
  assert result.ok() is True
  assert result.val() is None
