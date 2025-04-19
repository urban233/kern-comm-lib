import inspect
import sys
from typing import Callable, Optional
import kern_comm_lib as kern


def _get_caller_info(offset: int = 0) -> tuple[str, int]:
  """Get filename and line number of the caller."""
  frame = inspect.currentframe()
  try:
    for _ in range(2 + offset):
      if frame is None:
        break
      frame = frame.f_back

    if frame is None:
      return ("<unknown>", 0)

    return (frame.f_code.co_filename, frame.f_lineno)
  finally:
    # Clean up to avoid reference cycles
    del frame


def DCHECK(condition: Callable[[], bool],
           message: Optional[Callable[[], str]] = None) -> None:
  """Debug-only check removed in optimized mode.

  Similar to Abseil's DCHECK macro, this function checks a condition
  and terminates the program if the condition is false.

  Args:
      condition: A callable that returns the condition to check
      message: Optional callable that returns an error message
  """
  if __debug__:
    # Evaluate the condition lazily only in debug mode
    if not condition():
      # Get caller's frame information (skip this function's frame)
      frame = inspect.currentframe().f_back
      filename = frame.f_code.co_filename
      lineno = frame.f_lineno

      # Print the fatal error and exit
      print(f"FATAL ERROR: {filename}:{lineno}: {message()}", file=sys.stderr)
      exit(1)


if __name__ == '__main__':
    tmp_str = "Test"
    tmp_str2 = "Test1"
    DCHECK(lambda: tmp_str == "Test1", lambda: "String is not equal")
    print("Running in release")
