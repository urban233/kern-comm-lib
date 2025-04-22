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
File: threads/mutex.py
---------------------------------------------------------------------------

This file provides a framework-agnostic implementation of mutexes, allowing
the use of different locking mechanisms depending on the threading framework
(e.g., standard Python threading or PyQt6).
"""

import threading
from abc import ABC, abstractmethod

from kern_comm_lib.base import AStatusOrElse, Status, StatusCode
from kern_comm_lib.base.log import check

__docformat__ = "google"


class IMutex(ABC):
  """Abstract base class for mutex implementations."""

  @abstractmethod
  def acquire(
      self, blocking: bool = True, timeout: float = -1
  ) -> AStatusOrElse[bool]:
    """Acquires the mutex.

    Args:
      blocking (default: True): Whether to block until the mutex is acquired.
      timeout (default: -1): Maximum time to wait for the mutex in seconds.

    Returns:
      True if the mutex was acquired, False otherwise, if an error occurred
      a Status object is returned.
    """
    pass

  @abstractmethod
  def release(self) -> Status:
    """Releases the mutex."""
    pass

  def __enter__(self):
    """Context manager entry method. Acquires the mutex."""
    self.acquire()
    return self

  def __exit__(self, exc_type, exc_val, exc_tb):
    """Context manager exit method. Releases the mutex."""
    self.release()


class ThreadingMutex(IMutex):
  """Lock implementation using Python's threading.RLock.

  Attributes:
    _mutex: The underlying reentrant lock.
  """

  def __init__(self) -> None:
    """Initializes a new ThreadingMutex instance."""
    self._mutex: threading.RLock = threading.RLock()

  def acquire(
      self, blocking: bool = True, timeout: float = -1
  ) -> AStatusOrElse[bool]:
    """Acquires the mutex.

    Args:
      blocking (default: True): Whether to block until the mutex is acquired.
      timeout (default: -1): Maximum time to wait for the mutex in seconds.

    Returns:
      True if the mutex was acquired, False otherwise, if an error occurred
      a Status object is returned.
    """
    # <editor-fold desc="Checks">
    check.DCHECK_NOT_NONE(blocking)
    check.DCHECK_NOT_NONE(timeout)
    check.DCHECK_GREATER_THAN(timeout, 0)
    # </editor-fold>
    try:
      return self._mutex.acquire(blocking=blocking, timeout=timeout)
    except Exception as e:
      return Status.from_exception(e)

  def release(self) -> Status:
    """Releases the mutex.

    Returns:
      A Status object indicating success or failure of the operation.
    """
    try:
      self._mutex.release()
      return Status()
    except RuntimeError:
      return Status.from_status_code(
          StatusCode.FAILED_PRECONDITION,
          "Failed precondition: The mutex was not acquired.",
      )


class QtMutex(IMutex):
  """Lock implementation using PyQt6's QMutex.

  Attributes:
    _mutex: The underlying PyQt6 mutex.
  """

  def __init__(self) -> None:
    """Initializes a new QtMutex instance."""
    from PyQt6.QtCore import QMutex

    self._mutex: QMutex = QMutex()

  def acquire(
      self, blocking: bool = True, timeout: float = -1
  ) -> AStatusOrElse[bool]:
    """Acquires the mutex.

    Args:
      blocking (default: True): Whether to block until the mutex is acquired.
      timeout (default: -1): Maximum time to wait for the mutex in seconds.

    Returns:
      True if the mutex was acquired, False otherwise, if an error occurred
      a Status object is returned.
    """
    # <editor-fold desc="Checks">
    check.DCHECK_NOT_NONE(blocking)
    check.DCHECK_NOT_NONE(timeout)
    check.DCHECK_GREATER_THAN(timeout, 0)
    # </editor-fold>
    try:
      if timeout > 0:
        return self._mutex.tryLock(int(timeout * 1000))
      elif blocking:
        try:
          self._mutex.lock()
          return True
        except Exception:
          return Status.from_status_code(
              StatusCode.UNKNOWN,
              "Unknown error occurred while acquiring the mutex while blocking=True.",
          )
      else:
        return self._mutex.tryLock()
    except Exception as e:
      return Status.from_exception(e)

  def release(self) -> Status:
    """Releases the mutex.

    Returns:
      A Status object indicating success or failure of the operation.
    """
    try:
      self._mutex.unlock()
      return Status()
    except RuntimeError:
      return Status.from_status_code(
          StatusCode.FAILED_PRECONDITION,
          "Failed precondition: The mutex was not acquired.",
      )


class MutexFactory:
  """Factory class for creating mutex instances based on the selected implementation.

  Attributes:
    _mutex_class: The class to use for creating mutex instances.
  """

  _mutex_class: type[IMutex] = ThreadingMutex

  @classmethod
  def set_mutex_implementation(cls, lock_class: type[IMutex]) -> None:
    """Sets the mutex implementation to use.

    Args:
      lock_class: The mutex class to use for creating instances.
    """
    cls._mutex_class = lock_class

  @classmethod
  def create_mutex(cls) -> IMutex:
    """Creates a new mutex instance using the selected implementation.

    Returns:
      A new mutex instance.
    """
    return cls._mutex_class()
