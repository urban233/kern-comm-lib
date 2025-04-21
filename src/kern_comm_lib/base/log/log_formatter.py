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
  def __init__(self, format_pattern: str = None) -> None:
    """Constructor.

    Args:
      format_pattern: The pattern for formatting log messages. If None, a default pattern is used.

    Notes:
      Default pattern mimics GLog:
        - %severity% -> first letter of severity
        - %Y%m%d -> full date
        - %H:%M:%S.%f -> time with microseconds
        - [%F:%L] -> file name and line number of the log call
    """
    if format_pattern is None:
      format_pattern = "%severity%%Y%m%d %H:%M:%S.%f [%F:%L] "
    self.format_pattern = format_pattern

  def format(self, severity: log_severity.LogSeverity, message: str) -> str:
    now = datetime.datetime.now()
    stack = inspect.stack()
    if len(stack) > 5:
      caller_frame = stack[5]
      filename = caller_frame.filename.split("/")[-1]
      lineno = caller_frame.lineno
    else:
      filename = "unknown"
      lineno = -1

    mapping = {
      "%Y": f"{now.year:04d}",
      "%m": f"{now.month:02d}",
      "%d": f"{now.day:02d}",
      "%H": f"{now.hour:02d}",
      "%M": f"{now.minute:02d}",
      "%S": f"{now.second:02d}",
      "%f": f"{now.microsecond:06d}",
      "%severity%": severity.name[0] if severity.name else "?",
      "%F": filename,
      "%L": str(lineno)
    }

    formatted_prefix = self.format_pattern
    for key, value in mapping.items():
      formatted_prefix = formatted_prefix.replace(key, value)
    return f"{formatted_prefix}{message}"
