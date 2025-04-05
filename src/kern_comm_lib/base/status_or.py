from kern_comm_lib.base import status
from kern_comm_lib.base import status_code
from typing import Union


class StatusOr:
  """A class that holds a status and a value.

  This class is used to encapsulate a value that may either be a valid result or an error status.
  It provides methods to check the status and retrieve the value or error message.
  """

  def __init__(self, a_type: type, a_val_or_status: Union[object, status.Status] = None):
      self.type = a_type
      # Check if the second argument is a status
      if isinstance(a_val_or_status, status.Status):
          self.val = None
          self.status = a_val_or_status
      else:
          # Check if the val is of the correct type or None
          if a_val_or_status is not None and not isinstance(a_val_or_status, a_type):
              print(f"Expected value of type {a_type.__name__}, got {type(a_val_or_status).__name__}")
              exit(1)  # Crashes the program if the type is incorrect!
          self.val = a_val_or_status
          self.status = status_code.StatusCode.OK

  def ok(self) -> bool:
    """Check if the status is OK (no error)."""
    return self.status is status_code.StatusCode.OK
