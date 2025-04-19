"""
-----------------------------------------------------------------------------
File: log/check.py
-----------------------------------------------------------------------------

This file declares a family of `CHECK` macros.

`CHECK` macros terminate the program with a fatal error if the specified
condition is not true.

Except for those whose names begin with `DCHECK`, these macros are not
controlled by `NDEBUG` (cf. `assert`), so the check will be executed
regardless of compilation mode. `CHECK` and friends are thus useful for
confirming invariants in situations where continuing to run would be worse
than terminating, e.g., due to risk of data corruption or security
compromise.  It is also more robust and portable to deliberately terminate
at a particular place with a useful message and backtrace than to assume some
ultimately unspecified and unreliable crashing behavior (such as a
"segmentation fault").
"""
import inspect
from typing import Callable, Optional


def DCHECK(condition: Callable[[], bool],
           message: Optional[Callable[[], str]] = None) -> None:
  """Debug-only check removed in optimized mode.

  `DCHECK` behaves like `CHECK` in debug mode and does nothing otherwise (as
  `DLOG`).  Unlike with `CHECK` (but as with `assert`), it is not safe to rely
  on evaluation of `condition`: when `NDEBUG` is enabled, DCHECK does not
  evaluate the condition.

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
