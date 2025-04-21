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
File: base/log/logger.py
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

__docformat__ = "google"


class LogHandler(ABC):
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


class FileLogHandler(LogHandler):
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

    Raises:
        RuntimeError: If the log file cannot be opened.
        # TODO: Change to Status
    """
    self.file_path = file_path
    self._lock = threading.Lock()
    try:
      self.file = open(self.file_path, "a")
    except Exception as e:
      raise RuntimeError(f"Failed to open log file: {str(e)}")

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

  def close(self) -> None:
    """Closes the log file.

    Ensures that the file is properly closed, even if an exception occurs.
    """
    with self._lock:
      try:
        self.file.close()
      except Exception:
        pass
      # TODO: Add status


class ConsoleLogHandler(LogHandler):
  """Log handler that writes log messages to the console.

  Attributes:
    _lock: A lock to ensure thread-safe console access.
  """

  def __init__(self) -> None:
    """Constructor."""
    self._lock = threading.Lock()

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
      formatted_message = (
          f"{color_code}[{severity.name}] {message}{reset_code}\n"
      )

      with self._lock:
        sys.stdout.write(formatted_message)
        sys.stdout.flush()
      return Status()
    except Exception as e:
      return Status.from_exception(e)
