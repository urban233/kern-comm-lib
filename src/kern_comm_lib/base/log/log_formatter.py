"""Copyright 2025 by Martin Urban.

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
File: base/log/log_formatter.py
---------------------------------------------------------------------------

This file implements a basic log formatter that formats log messages
defaulting to a specified pattern used by the GLog library (C++).
"""

import datetime
import inspect
from kern_comm_lib.base.log import log_severity


class LogFormatter:
  """A class for formatting log messages with customizable patterns.

  This formatter allows developers to define a custom log message prefix
  format, similar to the GLog library. The format can include placeholders
  for date, time, severity, file name, and line number.

  Attributes:
    format_pattern (str): The pattern for formatting log messages. If None,
        a default pattern is used that mimics GLog.
  """

  def __init__(self, format_pattern: str = None) -> None:
    """Initializes the LogFormatter with a given format pattern.

    Args:
      format_pattern (default: None): The pattern for formatting log messages.

    Notes:
      Default pattern mimics GLog:
        - %severity% -> First letter of severity (e.g., I, W, E, F)
        - %Y%m%d -> Full date (year, month, day)
        - %H:%M:%S.%f -> Time with microseconds
        - [%F:%L] -> File name and line number of the log call
    """
    if format_pattern is None:
      format_pattern = "%severity%%Y%m%d %H:%M:%S.%f [%F:%L] "
    self.format_pattern = format_pattern

  def format(self, severity: log_severity.LogSeverity, message: str) -> str:
    """Formats a log message with the specified severity and message.

    This method generates a log message prefix based on the format pattern
    and replaces placeholders with actual values such as the current date,
    time, severity, file name, and line number.

    Args:
      severity: The severity level of the log message.
      message: The log message to be formatted.

    Returns:
      The formatted log message with the prefix.

    Notes:
      - The file name and line number are determined using the `inspect` module.
      - If the stack depth is insufficient, "unknown" and -1 are used as defaults
        for the file name and line number, respectively.
    """
    now = datetime.datetime.now()  # Get the current date and time
    stack = inspect.stack()  # Retrieve the call stack

    # Determine the caller's file name and line number
    if len(stack) > 5:
      caller_frame = stack[5]
      filename = caller_frame.filename.split("/")[-1]
      lineno = caller_frame.lineno
    else:
      filename = "unknown"
      lineno = -1

    # Mapping of placeholders to their corresponding values
    mapping = {
        "%Y": f"{now.year:04d}",  # Year (4 digits)
        "%m": f"{now.month:02d}",  # Month (2 digits)
        "%d": f"{now.day:02d}",  # Day (2 digits)
        "%H": f"{now.hour:02d}",  # Hour (2 digits)
        "%M": f"{now.minute:02d}",  # Minute (2 digits)
        "%S": f"{now.second:02d}",  # Second (2 digits)
        "%f": f"{now.microsecond:06d}",  # Microsecond (6 digits)
        "%severity%": severity.name[0]
        if severity.name
        else "?",  # First letter of severity
        "%F": filename,  # File name
        "%L": str(lineno),  # Line number
    }

    # Replace placeholders in the format pattern with actual values
    formatted_prefix = self.format_pattern
    for key, value in mapping.items():
      formatted_prefix = formatted_prefix.replace(key, value)

    # Return the formatted log message
    return f"{formatted_prefix}{message}"
