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

This file implements the basic logger class that is used by the LOG functions.
"""

import threading
from typing import TYPE_CHECKING, Optional

from kern_comm_lib.base import Status, StatusCode
from kern_comm_lib.base.log.check import DCHECK_IS_TYPE, DCHECK_NOT_NONE
from kern_comm_lib.base.log.log_handlers import ILogHandler
from kern_comm_lib.base.threads import mutex

if TYPE_CHECKING:
  from kern_comm_lib.base.log.log_severity import LogSeverity

__docformat__ = "google"


class Logger:
  """A thread-safe logger class that manages log handlers and provides logging functionality.

  Attributes:
    _instance_mutex: A mutex to ensure thread-safe access to the default logger instance.
    _default_instance: The default logger instance, shared across threads.
    _thread_local: Thread-local storage for logger instances.
    _handlers_registry: A registry of handlers for each logger.
    _registry_mutex: A lock to ensure thread-safe access to the handler's registry.
  """

  _instance_mutex = mutex.MutexFactory.create_mutex()
  _default_instance: Optional["Logger"] = None
  _thread_local = threading.local()
  _handlers_registry: dict[str, list["ILogHandler"]] = {}
  _registry_mutex = mutex.MutexFactory.create_mutex()

  def __init__(self, name: str = "default") -> None:
    """Constructor.

    Args:
      name (default: "default"): The name of the logger.
    """
    self.name = name
    self._handlers: list[ILogHandler] = []
    self._handlers_lock = mutex.MutexFactory.create_mutex()

    # Register the logger's handlers in a thread-safe manner to the global
    # default instance
    with Logger._registry_mutex:
      Logger._handlers_registry[name] = self._handlers

  def add_handler(self, handler: "ILogHandler") -> Status:
    """Adds a log handler to the logger.

    Args:
      handler: The log handler to add.

    Returns:
      A Status object indicating success or failure.
    """
    # <editor-fold desc="Checks">
    DCHECK_NOT_NONE(handler)
    DCHECK_IS_TYPE(handler, ILogHandler)
    # </editor-fold>

    try:
      # The context manager ensures that the mutex is released even if an exception occurs
      with self._handlers_lock:
        if handler not in self._handlers:
          self._handlers.append(handler)
      return Status()
    except Exception as e:
      return Status.from_exception(e)

  def remove_handler(self, handler: "ILogHandler") -> Status:
    """Removes a log handler from the logger.

    Args:
      handler: The log handler to remove.

    Returns:
      A Status object indicating success or failure.
    """
    # <editor-fold desc="Checks">
    DCHECK_NOT_NONE(handler)
    DCHECK_IS_TYPE(handler, ILogHandler)
    # </editor-fold>

    try:
      # The context manager ensures that the mutex is released even if an exception occurs
      with self._handlers_lock:
        if handler in self._handlers:
          self._handlers.remove(handler)
      return Status()
    except Exception as e:
      return Status.from_exception(e)

  def close_all_handlers(self) -> Status:
    """Closes all log handlers.

    Returns:
      A Status object indicating success or failure of the logging operation.
    """
    try:
      with self._handlers_lock:
        for handler in self._handlers:
          tmp_status: Status = handler.close()
          if not tmp_status.ok():
            return tmp_status
        self._handlers.clear()
      return Status()
    except Exception as e:
      return Status.from_exception(e)

  def log(self, severity: "LogSeverity", message: str) -> Status:
    """Logs a message with the specified severity level.

    Args:
      severity: The severity level of the log message.
      message: The log message to be recorded.

    Returns:
      A Status object indicating success or failure of the logging operation.
    """
    # <editor-fold desc="Checks">
    DCHECK_NOT_NONE(severity)
    DCHECK_NOT_NONE(message)
    # </editor-fold>

    # Get a snapshot of handlers to prevent modification during iteration
    try:
      with self._handlers_lock:
        if not self._handlers:
          return Status.from_status_code(
              StatusCode.NOT_FOUND, "No handlers configured"
          )
        # The shallow copy of the _handlers list is sufficient because:
        # We only need to protect against list modification (add/remove handlers)
        # The handler objects themselves are expected to handle their own thread safety
        handlers = self._handlers.copy()
    except Exception as e:
      return Status.from_exception(e)

    # Process handlers outside the lock
    try:
      for handler in handlers:
        tmp_status: Status = handler.handle(severity, message)
        if not tmp_status.ok():
          return tmp_status
      return Status()
    except Exception as e:
      return Status.from_exception(e)

  @classmethod
  def get_default(cls) -> "Logger":
    """Retrieves the default logger instance, creating it if necessary.

    Returns:
      The default logger instance.
    """
    with cls._instance_mutex:
      if cls._default_instance is None:
        cls._default_instance = cls("default")
      return cls._default_instance

  @classmethod
  def get_thread_logger(cls, name: str | None = None) -> "Logger":
    """Retrieves a thread-specific logger instance, creating it if necessary.

    Args:
      name (default: None): The name of the logger. If None, a name is generated based on the thread name.

    Returns:
      The thread-specific logger instance.
    """
    if not hasattr(cls._thread_local, "logger"):
      with cls._instance_mutex:
        thread_name = name or f"thread_{threading.current_thread().name}"
        cls._thread_local.logger = cls(thread_name)
    return cls._thread_local.logger

  @classmethod
  def cleanup_thread_logger(cls) -> None:
    """Cleans up the thread-local logger instance, removing it from the registry."""
    if hasattr(cls._thread_local, "logger"):
      with cls._registry_mutex:
        name = cls._thread_local.logger.name
        if name in cls._handlers_registry:
          del cls._handlers_registry[name]
      delattr(cls._thread_local, "logger")
