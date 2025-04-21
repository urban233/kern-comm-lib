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
File: threads/locks.py
---------------------------------------------------------------------------

This file provides a framework-agnostic implementation of locks, allowing
the use of different locking mechanisms depending on the threading framework
(e.g., standard Python threading or PyQt6).
"""

import threading
from abc import ABC, abstractmethod
from contextlib import contextmanager

__docformat__ = "google"


class LockInterface(ABC):
  """Abstract base class for lock implementations."""

  @abstractmethod
  def acquire(self, blocking: bool = True, timeout: float = -1) -> bool:
    """Acquires the lock.

    Args:
      blocking (default: True): Whether to block until the lock is acquired.
      timeout (default: None): Maximum time to wait for the lock in seconds.

    Returns:
      True if the lock was acquired, False otherwise.
    """
    pass

  @abstractmethod
  def release(self) -> None:
    """Releases the lock."""
    pass

  @contextmanager
  def __enter__(self):
    """Context manager entry method. Acquires the lock."""
    self.acquire()
    try:
      yield self
    finally:
      self.release()

  def __exit__(self, exc_type, exc_val, exc_tb):
    """Context manager exit method. Releases the lock."""
    self.release()


class ThreadingLock(LockInterface):
  """Lock implementation using Python's threading.RLock.

  Attributes:
    _lock (threading.RLock): The underlying reentrant lock.
  """

  def __init__(self) -> None:
    """Initializes a new ThreadingLock instance."""
    self._lock = threading.RLock()

  def acquire(self, blocking: bool = True, timeout: float = -1) -> bool:
    """Acquires the lock.

    Args:
      blocking (default: True): Whether to block until the lock is acquired.
      timeout (default: None): Maximum time to wait for the lock in seconds.

    Returns:
      True if the lock was acquired, False otherwise.
    """
    return self._lock.acquire(blocking=blocking, timeout=timeout)

  def release(self) -> None:
    """Releases the lock."""
    self._lock.release()


class QtLock(LockInterface):
  """Lock implementation using PyQt6's QMutex.

  Attributes:
    _lock (QMutex): The underlying PyQt6 mutex.
  """

  def __init__(self) -> None:
    """Initializes a new QtLock instance."""
    from PyQt6.QtCore import QMutex

    self._lock = QMutex()

  def acquire(self, blocking: bool = True, timeout: float = -1) -> bool:
    """Acquires the lock.

    Args:
      blocking (default: True): Whether to block until the lock is acquired.
      timeout (default: None): Maximum time to wait for the lock in seconds.

    Returns:
      True if the lock was acquired, False otherwise.
    """
    if timeout != -1:
      return self._lock.tryLock(int(timeout * 1000))
    elif blocking:
      return self._lock.lock()
    else:
      return self._lock.tryLock()

  def release(self) -> None:
    """Releases the lock."""
    self._lock.unlock()


class LockFactory:
  """Factory class for creating lock instances based on the selected implementation.

  Attributes:
    _lock_class: The class to use for creating lock instances.
  """

  _lock_class: type[LockInterface] = ThreadingLock

  @classmethod
  def set_lock_implementation(cls, lock_class: type[LockInterface]) -> None:
    """Sets the lock implementation to use.

    Args:
      lock_class: The lock class to use for creating instances.
    """
    cls._lock_class = lock_class

  @classmethod
  def create_lock(cls) -> LockInterface:
    """Creates a new lock instance using the selected implementation.

    Returns:
      A new lock instance.
    """
    return cls._lock_class()
