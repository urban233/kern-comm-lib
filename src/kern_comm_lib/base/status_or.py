from kern_comm_lib.base import status
from kern_comm_lib.base import status_code
from typing import Union, Optional


class StatusOr:
  """A container class that wraps either a value of a specified type or a Status object.

  StatusOr is used to handle operations that might fail, allowing functions to return
  either a value or an error status. This pattern eliminates the need for exceptions
  in many cases and makes error handling more explicit.

  Attributes:
      type: The expected type for the value.
      val: The value if the operation succeeded, None otherwise.
      status: A Status object representing the operation result.
          Will be an OK status if the operation succeeded.

  Example:
      ```python
      # Function returning StatusOr
      def divide(a: int, b: int) -> StatusOr:
          if b == 0:
              return StatusOr(float, Status.ZeroDivisionError("Division by zero!"))
          return StatusOr(float, a / b)

      # Using the StatusOr result
      result = divide(10, 2)
      if result.ok():
          print(f"Result: {result.val}")
      else:
          print(f"Error: {result.status}")
      ```
  """

  def __init__(
    self, a_type: type, a_val_or_status: Union[object, status.Status]
  ):
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
      self._val: Optional[object] = None
      self._status: "status.Status" = a_val_or_status
    else:
      # Check if the val is of the correct type or None
      if a_val_or_status is not None and not isinstance(
        a_val_or_status, a_type
      ):
        print(
          f"Expected value of type {a_type.__name__}, got {type(a_val_or_status).__name__}"
        )
        exit(1)  # Crashes the program if the type is incorrect!
      self._val = a_val_or_status
      self._status = status.Status()

  def ok(self) -> bool:
    """Checks if the StatusOr contains a valid value.

    Returns:
        True if the StatusOr contains a valid value, False if it contains an error.
    """
    return self._status.status_code() is status_code.StatusCode.OK

  def status(self) -> "status.Status":
    """Gets the Status object.

    Returns:
      The Status object representing the operation result.
    """
    return self._status

  def val(self) -> Optional[object]:
    """Gets the value.

    Returns:
      The value if the operation succeeded, None otherwise.
    """
    return self._val
