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
File: base/status/status_or.py
---------------------------------------------------------------------------

This file contains the StatusOr class.

A `kern.StatusOr` represents a class that holds a kern.Status object and
a possible value of a certain type.
The `kern.StatusOr` will either contain an object of a certain type
(indicating a successful operation), or an error (of type
`kern.Status`) explaining why such a value is not present.

In general, check the success of an operation returning an
`kern.StatusOr` like you would an `kern.Status` by using the `ok()`
member function.
"""

import sys

from kern_comm_lib.base.status import status, status_code


class StatusOr:
  """A container class that wraps either a value of a specified type or a Status object.

  StatusOr is used to handle operations that might fail, allowing functions to return
  either a value or an error status. This pattern eliminates the need for exceptions
  in many cases and makes error handling more explicit.

  Attributes:
    _type: The expected type for the value.
    _val: The value if the operation succeeded, None otherwise.
    _status: A Status object representing the operation result.
        Will be an OK status if the operation succeeded.
  """

  def __init__(
      self, a_type: type, a_val_or_status: object | status.Status
  ) -> None:
    """Constructor.

    Args:
      a_type: The expected type for the value.
      a_val_or_status: Either a value of type `a_type` or a Status object.
          If a value is provided, it must match the specified type.
          If a Status object is provided, it represents an error condition.

    Raises:
      SystemExit: If a value is provided that doesn't match the expected type.
    """
    self._type: type = a_type
    if isinstance(a_val_or_status, status.Status):
      self._val: object | None = None
      self._status: status.Status = a_val_or_status
    else:
      # Check if the val is of the correct type or None
      if a_val_or_status is not None and not isinstance(
          a_val_or_status, a_type
      ):
        print(
            f"Expected value of type {a_type.__name__}, got {type(a_val_or_status).__name__}"
        )
        sys.exit(1)  # Crashes the program if the type is incorrect!
      self._val = a_val_or_status
      self._status = status.Status()

  # <editor-fold desc="Alternative constructors">
  @staticmethod
  def from_exception(
      exception: Exception, include_traceback: bool = True
  ) -> "StatusOr":
    """Alternative constructor that creates a StatusOr object from a Python exception.

    Args:
      exception: The Python exception.
      include_traceback: Whether to include the exception's traceback.

    Returns:
        Status: A Status object with the appropriate status code, message, and optionally traceback.
    """
    tmp_status = status.Status(
        status_code.get_status_code_for_exception(exception), str(exception)
    )
    if include_traceback:
      tmp_status.set_traceback(
          status_code.format_exception_traceback(exception)
      )
    return StatusOr(None, tmp_status)  # type: ignore

  # </editor-fold>

  # <editor-fold desc="Public methods">
  # <editor-fold desc="Getter">
  def status(self) -> "status.Status":
    """Gets the Status object.

    Returns:
      The Status object representing the operation result.
    """
    return self._status

  def val(self) -> object | None:
    """Gets the value.

    Returns:
      The value if the operation succeeded, None otherwise.
    """
    return self._val

  # </editor-fold>

  def ok(self) -> bool:
    """Checks if the StatusOr contains a valid value.

    Returns:
        True if the StatusOr contains a valid value, False if it contains an error.
    """
    return self._status.status_code() is status_code.StatusCode.OK

  # </editor-fold>
