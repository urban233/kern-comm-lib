"""
Copyright 2025 by Martin Urban.

It is unlawful to modify or remove this copyright notice.
Licensed under the BSD-3-Clause;
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     https://opensource.org/license/bsd-3-clause

or please see the accompanying LICENSE file for further information.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

---------------------------------------------------------------------------
File: base/log/check.py
---------------------------------------------------------------------------

This file declares a family of `CHECK` macros.

`CHECK` "macros" (in Python terminology would these be check functions)
terminate the program with a fatal error if the specified condition is not true.

`DCHECK` "macros" (in Python terminology would these be dcheck functions)
terminate the program with a fatal error if the Python
code is run in debug mode (the default) and the condition is not true.
To disable the `DCHECK` macros, set the either the PYTHON_OPTIMIZE=1 or run
the Python script with the -O option. This will set the __debug__ variable to
False, which will disable the `DCHECK` macros.

`CHECK` and friends are thus useful for confirming invariants in situations
where continuing to run would be worse than terminating,
e.g., due to risk of data corruption or security compromise.
It is also more robust and portable to deliberately terminate
at a particular place with a useful message and backtrace than to assume some
ultimately unspecified and unreliable crashing behavior
(such as a "segmentation fault").
"""
import enum
import inspect
import sys
from typing import Callable, Optional, Type

# TODO: Add CHECK functions here

def DCHECK(condition: Callable[[], bool],
           message: Optional[Callable[[], str]] = None) -> None:
  """Debug-only check removed in optimized mode.

  `DCHECK` behaves like `CHECK` in debug mode and does nothing otherwise (as
  `DLOG`). It uses the `__debug__` variable to determine if the code is running
  in debug mode and uses lazy evaluation of the condition to have no runtime
  overhead in release builds. However, this requires the condition to be a
  lambda function (see Examples).

  Args:
      condition: A callable that returns the condition to check
      message: Optional callable that returns an error message

  Examples:
    A simple example of how to use `DCHECK`:
      >>> import kern_comm_lib as kern
      >>> tmp_str = "Test"
      >>> kern.DCHECK(lambda: tmp_str == "Test1", lambda: "String is not equal")
    In production, use more specific DCHECK functions like DCHECK_EQ or DCHECK_NOT_EQ
    for simple comparisons.
  """
  if __debug__:
    # Evaluate the condition lazily only in debug mode
    if not condition():
      # Get caller's frame information which cannot be placed in its own
      # function because it would use the wrong function's frame!
      frame = inspect.currentframe().f_back
      filename = frame.f_code.co_filename
      lineno = frame.f_lineno
      # Print the fatal error and exit
      print(f"FATAL ERROR: {filename}:{lineno}: {message()}", file=sys.stderr)
      exit(1)


def DCHECK_EQ(arg1: object, arg2: object):
  """Checks if two values are equal."""
  if __debug__:
    if arg1 != arg2:
      # Get caller's frame information which cannot be placed in its own
      # function because it would use the wrong function's frame!
      frame = inspect.currentframe().f_back
      filename = frame.f_code.co_filename
      lineno = frame.f_lineno
      # Print the fatal error and exit
      print(f"FATAL ERROR: {filename}:{lineno}: {arg1} is NOT equal to {arg2}", file=sys.stderr)
      exit(1)


def DCHECK_NOT_EQ(arg1: object, arg2: object):
  """Checks if two values are equal."""
  if __debug__:
    if arg1 == arg2:
      # Get caller's frame information which cannot be placed in its own
      # function because it would use the wrong function's frame!
      frame = inspect.currentframe().f_back
      filename = frame.f_code.co_filename
      lineno = frame.f_lineno
      # Print the fatal error and exit
      print(f"FATAL ERROR: {filename}:{lineno}: {arg1} is equal to {arg2}", file=sys.stderr)
      exit(1)


def DCHECK_NOT_NONE(val: object):
  """Checks if a value is not None."""
  if __debug__:
    if val is None:
      # Get caller's frame information which cannot be placed in its own
      # function because it would use the wrong function's frame!
      frame = inspect.currentframe().f_back
      filename = frame.f_code.co_filename
      lineno = frame.f_lineno
      # Print the fatal error and exit
      print(f"FATAL ERROR: {filename}:{lineno}: Value should not be None", file=sys.stderr)
      exit(1)


def DCHECK_IN_ENUM(a_val: object, an_enum_class: Type['enum.IntEnum']) -> None:
  """Debug-only check that verifies if a value is a member of the specified enum.

  Args:
      a_val: The value to check
      an_enum_class: The enum class to check against
  """
  if __debug__:
    try:
      an_enum_class(a_val)  # This will raise ValueError if val is not in the enum
    except ValueError:
      # Get caller's frame information which cannot be placed in its own
      # function because it would use the wrong function's frame!
      frame = inspect.currentframe().f_back
      filename = frame.f_code.co_filename
      lineno = frame.f_lineno
      # Print the fatal error and exit
      print(f"FATAL ERROR: {filename}:{lineno}: Value {a_val} is not a valid member of enum {an_enum_class.__name__}", file=sys.stderr)
      exit(1)

# TODO: Add more DCHECK functions here
