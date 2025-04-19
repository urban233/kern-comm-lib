"""
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
These canonical codes are understood across the codebase
"""
# A* -------------------------------------------------------------------
# B* This file contains source code for the Kern - Common Python
# -* Libraries project.
# C* Copyright 2025 by Martin Urban.
# D* -------------------------------------------------------------------
# E* It is unlawful to modify or remove this copyright notice.
# F* -------------------------------------------------------------------
# G* Please see the accompanying LICENSE file for further information.
# H* -------------------------------------------------------------------
# I* Additional authors of this source file include:
# -*
# -*
# -*
# Z* -------------------------------------------------------------------
from typing import Union, Optional, Any, Callable
from functools import wraps

from kern_comm_lib.status import status_code

__docformat__ = "google"


class Status:
  """A class that represents the status of an operation."""

  def __init__(
          self,
          a_status_code: status_code.StatusCode = status_code.StatusCode.OK,
          a_message: Optional[str] = None,
  ):
    """Constructor.

    Args:
      a_status_code: An optional status code (default: Ok).
      a_message: An optional message describing the status.
    """
    self._status_code: "status_code.StatusCode" = a_status_code
    self._message: Optional[str] = a_message
    self._traceback: Optional[str] = None

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
        status_code.StatusCode: The status code.
    """
    return self._status_code

  def message(self) -> Optional[str]:
    """Gets the message.

    Returns:
      The message.
    """
    return self._message

  def traceback(self) -> Optional[str]:
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


def use_status(func: Callable[..., Any]) -> Callable[..., Union[Any, Status]]:
  """Decorator that wraps a function and converts exceptions to StatusOr objects."""
  @wraps(func)
  def wrapper(*args: Any, **kwargs: Any) -> Union[Any, Status]:
    try:
      return func(*args, **kwargs)
    except Exception as e:
      return Status.from_exception(e)
  return wrapper


# <editor-fold desc="Error functions">
def custom_error(
        error_code: "status_code.StatusCode", message: Optional[str] = None
) -> "Status":
  """Creates a custom error status.

  Args:
      error_code (status_code.StatusCode): The custom error code.
      message (Optional[str]): An optional message describing the error.

  Returns:
      Status: A Status object with the custom error code and message.
  """
  return Status(error_code, message)


def invalid_argument_error(message: Optional[str] = None) -> "Status":
  """Creates an invalid argument error status.

  Args:
      message (Optional[str]): An optional message describing the error.

  Returns:
      Status: A Status object with the INVALID_ARGUMENT error code and message.
  """
  return Status(status_code.StatusCode.INVALID_ARGUMENT, message)


def not_found_error(message: Optional[str] = None) -> "Status":
  """Creates a not found error status.

  Args:
      message (Optional[str]): An optional message describing the error.

  Returns:
      Status: A Status object with the NOT_FOUND error code and message.
  """
  return Status(status_code.StatusCode.NOT_FOUND, message)


def zero_division_error(message: Optional[str] = None) -> "Status":
  """Creates a zero division error status.

  Args:
      message (Optional[str]): An optional message describing the error.

  Returns:
      Status: A Status object with the ZERO_DIVISION error code and message.
  """
  return Status(status_code.StatusCode.ZERO_DIVISION, message)
# </editor-fold>
