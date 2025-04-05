from typing import Optional

from kern_comm_lib.base import status_code

__docformat__ = "google"


class Status:
  """A class that represents the status of an operation."""

  def __init__(self, code: status_code.StatusCode = status_code.StatusCode.OK, message:Optional[str] = None):
    """Constructor.

    Args:
      code: The status code.
      message (Optional): An optional message describing the status.
    """
    self.code = code
    self.message = message

  def ok(self):
    return self.code == status_code.StatusCode.OK

  def code(self):
    return self.code

  def __str__(self):
    if self.ok():
      return "OK"
    return f"{self.code.name}: {self.message}" if self.message else self.code.name

  def __eq__(self, other):
    if not isinstance(other, Status):
      return False
    return self.code == other.code and self.message == other.message

  @staticmethod
  def CustomError(error_code: "status_code.StatusCode", message=None):
    return Status(error_code, message)

  @staticmethod
  def InvalidArgumentError(message=None):
    return Status(status_code.StatusCode.INVALID_ARGUMENT, message)

  @staticmethod
  def NotFoundError(message=None):
    return Status(status_code.StatusCode.NOT_FOUND, message)

  @staticmethod
  def ZeroDivisionError(message=None):
    return Status(status_code.StatusCode.ZERO_DIVISION, message)
