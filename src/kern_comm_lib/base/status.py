from typing import Optional

from kern_comm_lib.base import status_code

__docformat__ = "google"


class Status:
  """A class that represents the status of an operation."""

  def __init__(
          self,
          a_status_code: status_code.StatusCode = status_code.StatusCode.OK,
          message: Optional[str] = None,
  ):
    """Constructor.

    Args:
        code: The status code.
        message: An optional message describing the status.
    """
    self._status_code: "status_code.StatusCode" = a_status_code
    self._message: Optional[str] = message
    self._traceback: Optional[str] = None

  @staticmethod
  def from_exception(
          exception: Exception, include_traceback: bool = True
  ) -> "Status":
    """Creates a Status object from a Python exception.

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

  def ok(self) -> bool:
    """Checks if the status is OK.

    Returns:
        bool: True if the status code is OK, False otherwise.
    """
    return self._status_code == status_code.StatusCode.OK

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

  def set_traceback(self, a_traceback: str) -> None:
    """Sets the traceback for the status.

    Args:
        a_traceback: The traceback string.
    """
    self._traceback = a_traceback


def CustomError(
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


def InvalidArgumentError(message: Optional[str] = None) -> "Status":
  """Creates an invalid argument error status.

  Args:
      message (Optional[str]): An optional message describing the error.

  Returns:
      Status: A Status object with the INVALID_ARGUMENT error code and message.
  """
  return Status(status_code.StatusCode.INVALID_ARGUMENT, message)


def NotFoundError(message: Optional[str] = None) -> "Status":
  """Creates a not found error status.

  Args:
      message (Optional[str]): An optional message describing the error.

  Returns:
      Status: A Status object with the NOT_FOUND error code and message.
  """
  return Status(status_code.StatusCode.NOT_FOUND, message)


def ZeroDivisionError(message: Optional[str] = None) -> "Status":
  """Creates a zero division error status.

  Args:
      message (Optional[str]): An optional message describing the error.

  Returns:
      Status: A Status object with the ZERO_DIVISION error code and message.
  """
  return Status(status_code.StatusCode.ZERO_DIVISION, message)
