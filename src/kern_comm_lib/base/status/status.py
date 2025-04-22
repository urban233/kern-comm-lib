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
File: base/status/status.py
---------------------------------------------------------------------------

Within PySSA, `kern.Status` is the primary mechanism for communicating
errors in Python, and is used to represent an error state
Some of these errors may be recoverable, but others may not.
Most functions that can produce a recoverable error
should be designed to return an `kern.Status` (or `kern.StatusOr`).

A `kern.Status` is designed to either return "OK" or one of a number of
different error codes, corresponding to typical error conditions.
In almost all cases, when using `kern.Status` you should use the canonical
error codes (of type `kern.StatusCode`) enumerated in the status_code
python module.
These canonical codes are understood across the codebase.
"""

from collections.abc import Callable
from functools import wraps
from typing import Any

from kern_comm_lib.base.status import status_code

__docformat__ = "google"


class Status:
  """A class that represents the status of an operation.

  Attributes:
    _status_code: The status code of the operation.
    _message: An optional message describing the status.
    _traceback: An optional traceback string.
  """

  def __init__(
      self,
      a_status_code: status_code.StatusCode = status_code.StatusCode.OK,
      a_message: str | None = None,
  ):
    """Constructor.

    Args:
      a_status_code: An optional status code (default: Ok).
      a_message: An optional message describing the status.
    """
    self._status_code: status_code.StatusCode = a_status_code
    self._message: str | None = a_message
    self._traceback: str | None = None

  # <editor-fold desc="Alternative constructors">
  @staticmethod
  def from_exception(
      exception: Exception, include_traceback: bool = True
  ) -> "Status":
    """Alternative constructor that creates a Status object from a Python exception.

    Args:
        exception: The Python exception.
        include_traceback: Whether to include the exception's traceback.

    Returns:
        Status: A Status object with the appropriate status code, message, and optionally traceback.
    """
    tmp_status = Status(
        status_code.get_status_code_for_exception(exception), str(exception)
    )
    if include_traceback:
      tmp_status.set_traceback(
          status_code.format_exception_traceback(exception)
      )
    return tmp_status

  @staticmethod
  def from_status_code(
      a_status_code: status_code.StatusCode,
      a_message: str | None = None,
  ) -> "Status":
    """Alternative constructor that creates a Status object from a status code.

    Args:
        a_status_code: The status code.
        a_message: An optional message describing the status.

    Returns:
        A Status object with the specified status code and message.
    """
    return Status(a_status_code, a_message)

  # </editor-fold>

  # <editor-fold desc="Magic methods">
  def __str__(self) -> str:
    """Gets the string representation of the status.

    Returns:
        str: "OK" if the status is OK, otherwise the status code name and message.
    """
    if self.ok():
      return "OK"
    return (
        f"{self._status_code.name}: {self._message}"
        if self._message
        else self._status_code.name
    )

  # </editor-fold>

  # <editor-fold desc="Public methods">
  def ok(self) -> bool:
    """Checks if the status is OK.

    Returns:
        bool: True if the status code is OK, False otherwise.
    """
    return self._status_code == status_code.StatusCode.OK

  # <editor-fold desc="Getter">
  def status_code(self) -> status_code.StatusCode:
    """Gets the status code.

    Returns:
      The status code.
    """
    return self._status_code

  def message(self) -> str | None:
    """Gets the message.

    Returns:
      The message.
    """
    return self._message

  def traceback(self) -> str | None:
    """Gets the traceback."""
    return self._traceback

  # </editor-fold>

  # <editor-fold desc="Setter">
  def set_traceback(self, a_traceback: str) -> None:
    """Sets the traceback for the status.

    Args:
        a_traceback: The traceback string.
    """
    self._traceback = a_traceback

  # </editor-fold>
  # </editor-fold>


# <editor-fold desc="Decorators">
def use_status(func: Callable[..., Any]) -> Callable[..., Any | Status]:
  """Decorator that wraps a function and converts exceptions to StatusOr objects."""

  @wraps(func)
  def wrapper(*args: Any, **kwargs: Any) -> Any | Status:
    try:
      return func(*args, **kwargs)
    except Exception as e:
      return Status.from_exception(e)

  return wrapper


# </editor-fold>


# <editor-fold desc="Error functions">
def invalid_argument_error(message: str | None = None) -> "Status":
  """Creates an invalid argument error status.

  Args:
      message (Optional[str]): An optional message describing the error.

  Returns:
      Status: A Status object with the INVALID_ARGUMENT error code and message.
  """
  return Status(status_code.StatusCode.INVALID_ARGUMENT, message)


def not_found_error(message: str | None = None) -> "Status":
  """Creates a not found error status.

  Args:
      message (Optional[str]): An optional message describing the error.

  Returns:
      Status: A Status object with the NOT_FOUND error code and message.
  """
  return Status(status_code.StatusCode.NOT_FOUND, message)


def zero_division_error(message: str | None = None) -> "Status":
  """Creates a zero division error status.

  Args:
      message (Optional[str]): An optional message describing the error.

  Returns:
      Status: A Status object with the ZERO_DIVISION error code and message.
  """
  return Status(status_code.StatusCode.ZERO_DIVISION, message)


# </editor-fold>
