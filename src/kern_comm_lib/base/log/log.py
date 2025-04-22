# Copyright 2025 by Martin Urban.
#
# It is unlawful to modify or remove this copyright notice.
# Licensed under the BSD-3-Clause;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://opensource.org/license/bsd-3-clause
#
# or please see the accompanying LICENSE file for further information.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
---------------------------------------------------------------------------
File: base/log/log.py
---------------------------------------------------------------------------

This file declares a family of LOG functions.

Most `LOG` macros take a severity level argument.  The severity levels are
`INFO`, `WARNING`, `ERROR`, and `FATAL`.  They are defined
in base/log/log_severity.py.
"""

import sys

from kern_comm_lib.base import Status
from kern_comm_lib.base.log.check import DCHECK_NOT_NONE
from kern_comm_lib.base.log.log_handlers import (
    ConsoleLogHandler,
    FileLogHandler,
)
from kern_comm_lib.base.log.log_severity import (
    ERROR,
    FATAL,
    INFO,
    WARNING,
    LogSeverity,
)
from kern_comm_lib.base.log.logger import Logger

__docformat__ = "google"


_initialized = False  # Tracks whether the logging system has been initialized


def init_kern_logging(program_name: str, log_dir: str = "") -> Status:
  """Initializes the logging system with a default logger and handlers.

  Args:
    program_name: The name of the program, used for naming log files.
    log_dir (default: ""): The directory where log files will be stored. If None, no file handler is added.

  Returns:
    A Status object indicating success or failure of the initialization process.
  """
  # <editor-fold desc="Checks">
  DCHECK_NOT_NONE(log_dir)
  # </editor-fold>

  global _initialized  # noqa: PLW0603 (module level variable is the simplest way to track initialization)
  if _initialized:
    return Status()  # Return success if already initialized

  logger = Logger.get_default()

  # Always add a console handler to the logger
  tmp_status = logger.add_handler(ConsoleLogHandler())
  if not tmp_status.ok():
    return tmp_status

  # Add a file handler if a log directory is provided
  if log_dir != "":
    try:
      import os

      os.makedirs(log_dir, exist_ok=True)  # Ensure the log directory exists
      log_path = os.path.join(
          log_dir, f"{program_name}.log"
      )  # Construct the log file path
      file_handler = FileLogHandler(log_path)
      status = logger.add_handler(file_handler)
      if not status.ok():
        return status
    except Exception as e:
      return Status.from_exception(e)

  _initialized = True  # Mark the logging system as initialized
  return Status()


def close_kern_logging() -> Status:
  """Closes all log handlers and releases resources.

  Returns:
    A Status object indicating success or failure of the operation.
  """
  logger = Logger.get_default()
  status = logger.close_all_handlers()
  if not status.ok():
    return status

  global _initialized  # noqa: PLW0603 (module level variable is the simplest way to track initialization)
  _initialized = False  # Mark the logging system as uninitialized
  return Status()


def init_thread_specific_kern_logging(log_dir: str = "") -> Status:
  """Initializes the logging system with a thread-specific logger and handlers.

  Args:
    log_dir (default: ""): The directory where log files will be stored. If None, no file handler is added.

  Returns:
    A Status object indicating success or failure of the initialization process.
  """
  # <editor-fold desc="Checks">
  DCHECK_NOT_NONE(log_dir)
  # </editor-fold>

  logger = Logger.get_thread_logger()
  # Always add a console handler to the logger
  tmp_status = logger.add_handler(ConsoleLogHandler())
  if not tmp_status.ok():
    return tmp_status

  # Add a file handler if a log directory is provided
  if log_dir != "":
    try:
      import os

      os.makedirs(log_dir, exist_ok=True)  # Ensure the log directory exists
      log_path = os.path.join(
          log_dir, f"{logger.name}.log"
      )  # Construct the log file path
      file_handler = FileLogHandler(log_path)
      status = logger.add_handler(file_handler)
      if not status.ok():
        return status
    except Exception as e:
      return Status.from_exception(e)
  return Status()


def close_thread_specific_kern_logging() -> Status:
  """Closes all log handlers and releases resources that belong to a thread specific logger.

  Returns:
    A Status object indicating success or failure of the operation.
  """
  logger = Logger.get_thread_logger()
  status = logger.close_all_handlers()
  if not status.ok():
    return status

  global _initialized  # noqa: PLW0603 (module level variable is the simplest way to track initialization)
  _initialized = False  # Mark the logging system as uninitialized
  return Status()


# <editor-fold desc="LOG functions">
def LOG(severity: LogSeverity, message: str) -> Status:
  """Logs a message with the specified severity level.

  Args:
    severity: The severity level of the log message (e.g., INFO, WARNING, ERROR, FATAL).
    message: The log message to be recorded.

  Returns:
    A Status object indicating success or failure of the logging operation.
  """
  return Logger.get_default().log(severity, message)


def LOG_INFO(message: str) -> Status:
  """Logs an informational message.

  Args:
    message: The log message to be recorded.

  Returns:
    A Status object indicating success or failure of the logging operation.
  """
  return LOG(INFO, message)


def LOG_WARNING(message: str) -> Status:
  """Logs a warning message.

  Args:
    message: The log message to be recorded.

  Returns:
    A Status object indicating success or failure of the logging operation.
  """
  return LOG(WARNING, message)


def LOG_ERROR(message: str) -> Status:
  """Logs an error message.

  Args:
    message: The log message to be recorded.

  Returns:
    A Status object indicating success or failure of the logging operation.
  """
  return LOG(ERROR, message)


def LOG_FATAL(message: str) -> None:
  """Logs a fatal error message and terminates the program.

  Args:
    message: The log message to be recorded.

  Notes:
    This function will terminate the program after logging the message.
  """
  LOG(FATAL, message)
  import sys

  sys.exit(1)  # Terminate the program in case of a fatal error


# </editor-fold>


# <editor-fold desc="DLOG functions">
def DLOG(severity: LogSeverity, message: str) -> None:
  """Logs a message with the specified severity level in debug mode.

  Args:
    severity: The severity level of the log message (e.g., INFO, WARNING, ERROR, FATAL).
    message: The log message to be recorded.

  Notes:
    It exits the program if the logging operation fails.
    This function returns None if the logging operation is successful. This has
    to be done instead of a Status object, because if the operation fails
    the program will be terminated.
  """
  if __debug__:
    tmp_status = Logger.get_default().log(severity, message)
    if not tmp_status.ok():
      sys.exit(1)


def DLOG_INFO(message: str) -> None:
  """Logs an informational message in debug mode.

  Args:
    message: The log message to be recorded.

  Notes:
    It exits the program if the logging operation fails.
  """
  if __debug__:
    tmp_status = LOG(INFO, message)
    if not tmp_status.ok():
      sys.exit(1)


def DLOG_WARNING(message: str) -> None:
  """Logs a warning message in debug mode.

  Args:
    message: The log message to be recorded.

  Notes:
    It exits the program if the logging operation fails.
  """
  if __debug__:
    tmp_status = LOG(WARNING, message)
    if not tmp_status.ok():
      sys.exit(1)


def DLOG_ERROR(message: str) -> None:
  """Logs an error message in debug mode.

  Args:
    message: The log message to be recorded.

  Notes:
    It exits the program if the logging operation fails.
  """
  if __debug__:
    tmp_status = LOG(ERROR, message)
    if not tmp_status.ok():
      sys.exit(1)


def DLOG_FATAL(message: str) -> None:
  """Logs a fatal error message in debug mode and terminates the program.

  Args:
    message: The log message to be recorded.

  Notes:
    It exits the program if the logging operation fails.
    This function will terminate the program after logging the message.
  """
  if __debug__:
    DLOG(FATAL, message)
    sys.exit(1)


# </editor-fold>


# <editor-fold desc="TLOG functions">
def TLOG(severity: LogSeverity, message: str) -> Status:
  """Logs a message with the specified severity level using thread-specific logger.

  Args:
    severity: The severity level of the log message (e.g., INFO, WARNING, ERROR, FATAL).
    message: The log message to be recorded.

  Returns:
    A Status object indicating success or failure of the logging operation.
  """
  return Logger.get_thread_logger().log(severity, message)


def TLOG_INFO(message: str) -> Status:
  """Logs an informational message using thread-specific logger.

  Args:
    message: The log message to be recorded.

  Returns:
    A Status object indicating success or failure of the logging operation.
  """
  return TLOG(INFO, message)


def TLOG_WARNING(message: str) -> Status:
  """Logs a warning message using thread-specific logger.

  Args:
    message: The log message to be recorded.

  Returns:
    A Status object indicating success or failure of the logging operation.
  """
  return TLOG(WARNING, message)


def TLOG_ERROR(message: str) -> Status:
  """Logs an error message using thread-specific logger.

  Args:
    message: The log message to be recorded.

  Returns:
    A Status object indicating success or failure of the logging operation.
  """
  return TLOG(ERROR, message)


def TLOG_FATAL(message: str) -> None:
  """Logs a fatal error message using thread-specific logger and terminates the program.

  Args:
    message: The log message to be recorded.

  Notes:
    This function will terminate the program after logging the message.
  """
  TLOG(FATAL, message)
  import sys

  sys.exit(1)  # Terminate the program in case of a fatal error


# </editor-fold>


# <editor-fold desc="DTLOG functions">
def DTLOG(severity: LogSeverity, message: str) -> None:
  """Logs a message with the specified severity level in debug mode using thread-specific logger.

  Args:
    severity: The severity level of the log message (e.g., INFO, WARNING, ERROR, FATAL).
    message: The log message to be recorded.

  Notes:
    It exits the program if the logging operation fails.
    This function returns None if the logging operation is successful. This has
    to be done instead of a Status object, because if the operation fails
    the program will be terminated.
  """
  if __debug__:
    tmp_status = Logger.get_thread_logger().log(severity, message)
    if not tmp_status.ok():
      sys.exit(1)


def DTLOG_INFO(message: str) -> None:
  """Logs an informational message in debug mode using thread-specific logger.

  Args:
    message: The log message to be recorded.

  Notes:
    It exits the program if the logging operation fails.
  """
  if __debug__:
    tmp_status = TLOG(INFO, message)
    if not tmp_status.ok():
      sys.exit(1)


def DTLOG_WARNING(message: str) -> None:
  """Logs a warning message in debug mode using thread-specific logger.

  Args:
    message: The log message to be recorded.

  Notes:
    It exits the program if the logging operation fails.
  """
  if __debug__:
    tmp_status = TLOG(WARNING, message)
    if not tmp_status.ok():
      sys.exit(1)


def DTLOG_ERROR(message: str) -> None:
  """Logs an error message in debug mode using thread-specific logger.

  Args:
    message: The log message to be recorded.

  Notes:
    It exits the program if the logging operation fails.
  """
  if __debug__:
    tmp_status = TLOG(ERROR, message)
    if not tmp_status.ok():
      sys.exit(1)


def DTLOG_FATAL(message: str) -> None:
  """Logs a fatal error message in debug mode using thread-specific logger and terminates the program.

  Args:
    message: The log message to be recorded.

  Notes:
    It exits the program if the logging operation fails.
    This function will terminate the program after logging the message.
  """
  if __debug__:
    DTLOG(FATAL, message)
    sys.exit(1)


# </editor-fold>
