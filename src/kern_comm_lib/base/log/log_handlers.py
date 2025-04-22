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
File: base/log/log_handlers.py
---------------------------------------------------------------------------

This file implements two log handlers:
- FileLogHandler: Writes log messages to a file.
- ConsoleLogHandler: Writes log messages to the console with color formatting.
"""

import sys
import threading
from abc import ABC, abstractmethod

from kern_comm_lib.base import Status
from kern_comm_lib.base.log import log_severity
from kern_comm_lib.base.log.log_formatter import LogFormatter

__docformat__ = "google"


class ILogHandler(ABC):
  """Abstract base class for log handlers."""

  @abstractmethod
  def handle(
      self, severity: "log_severity.LogSeverity", message: str
  ) -> Status:
    """Handles a log message.

    Args:
      severity: The severity level of the log message.
      message: The log message to be handled.

    Returns:
      A Status object indicating success or failure of the operation.
    """
    pass

  def close(self) -> Status:
    """Closes the log handler.

    This method should be overridden by subclasses to implement any necessary
    cleanup operations when the handler is no longer needed.
    """
    return Status()


class FileLogHandler(ILogHandler):
  """Log handler that writes log messages to a file.

  Attributes:
      file_path: The path to the log file.
      _lock: A lock to ensure thread-safe file access.
      file: The file object for the log file.
  """

  def __init__(self, file_path: str) -> None:
    """Initializes a FileLogHandler instance.

    Args:
      file_path: The path to the log file.
    """
    self.file_path = file_path
    self._lock = threading.Lock()
    try:
      # self.file should contain the file object, therefore opening the
      # file_path using a context manager is not applicable here.
      self.file = open(self.file_path, "a")  # noqa: SIM115 (see above)
    except Exception as e:
      print(f"Failed to open log file: {str(e)}")
      sys.exit(1)

  def handle(
      self, severity: "log_severity.LogSeverity", message: str
  ) -> Status:
    """Writes a log message to the file.

    Args:
      severity: The severity level of the log message.
      message: The log message to be written.

    Returns:
      A Status object indicating success or failure of the operation.
    """
    try:
      with self._lock:
        self.file.write(f"[{severity.name}] {message}\n")
        self.file.flush()
      return Status()
    except Exception as e:
      return Status.from_exception(e)

  def close(self) -> Status:
    """Closes the log file.

    Ensures that the file is properly closed, even if an exception occurs.
    """
    with self._lock:
      try:
        self.file.close()
        return Status()
      except Exception as e:
        return Status.from_exception(e)


class ConsoleLogHandler(ILogHandler):
  """Log handler that writes log messages to the console.

  Attributes:
    _lock: A lock to ensure thread-safe console access.
  """

  def __init__(self, format_pattern: str | None = None) -> None:
    """Constructor.

    Args:
      format_pattern: Optional format string for log messages
    """
    self._lock = threading.Lock()
    self._formatter = LogFormatter(format_pattern)

  def handle(
      self, severity: "log_severity.LogSeverity", message: str
  ) -> Status:
    """Writes a log message to the console with color formatting.

    Args:
      severity: The severity level of the log message.
      message: The log message to be written.

    Returns:
      A Status object indicating success or failure of the operation.
    """
    try:
      color_code = {
          log_severity.INFO: "\033[0m",  # Default color
          log_severity.WARNING: "\033[33m",  # Yellow
          log_severity.ERROR: "\033[31m",  # Red
          log_severity.FATAL: "\033[35m",  # Magenta
      }.get(severity, "\033[0m")

      reset_code = "\033[0m"  # Reset color
      formatted_message = self._formatter.format(severity, message)
      formatted_message_with_color = (
          f"{color_code}{formatted_message}{reset_code}\n"
      )

      with self._lock:
        sys.stdout.write(formatted_message_with_color)
        sys.stdout.flush()
      return Status()
    except Exception as e:
      return Status.from_exception(e)
