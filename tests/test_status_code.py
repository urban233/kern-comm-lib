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
File: tests/test_status_code.py
---------------------------------------------------------------------------

This file defines a number of tests to verify the functionality of the
status code module.
"""

import kern_comm_lib as kern
from kern_comm_lib.base.status import status_code


def test_status_code_ok() -> None:
  """Tests that the OK status code has the expected value of 0."""
  assert kern.StatusCode.OK == 0


def test_status_code_invalid_argument() -> None:
  """Tests that the INVALID_ARGUMENT status code has the expected value of 3."""
  assert kern.StatusCode.INVALID_ARGUMENT == 3  # noqa: PLR2004


def test_get_status_code_for_known_exception() -> None:
  """Tests that a known exception (ValueError) maps to the correct status code."""
  assert (
      status_code.get_status_code_for_exception(ValueError())
      == kern.StatusCode.VALUE_ERROR
  )


def test_get_status_code_for_unknown_exception() -> None:
  """Tests that an unknown custom exception maps to the UNKNOWN status code."""

  class CustomException(Exception):
    pass

  assert (
      status_code.get_status_code_for_exception(CustomException())
      == kern.StatusCode.UNKNOWN
  )


def test_format_exception_traceback_contains_message() -> None:
  """Tests that the formatted exception traceback includes the exception message."""
  try:
    raise ValueError("Test error")
  except ValueError as e:
    formatted_traceback = status_code.format_exception_traceback(e)
    assert "Test error" in formatted_traceback


def test_format_exception_traceback_contains_traceback() -> None:
  """Tests that the formatted exception traceback includes traceback information."""
  try:
    raise ValueError("Test error")
  except ValueError as e:
    formatted_traceback = status_code.format_exception_traceback(e)
    assert "Traceback" in formatted_traceback
