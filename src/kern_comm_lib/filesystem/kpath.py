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
File: filesystem/kpath.py
---------------------------------------------------------------------------

The pathlib.Path class is commonly used for file and directory operations
in Python. To provide a consistent interface for file system operations,
that does not use exceptions, a wrapper class is created called KPath.
This class wraps the pathlib.Path class and provides methods for file and
directory operations, such as creating directories, reading and writing files,
and checking file existence. The KPath class also provides a way to set
file permissions using the FilesystemModes enum.

The interface of the KPath class is kept very similar to the pathlib.Path class
to enable a drop-in replacement. Therefore, the migration to the KPath class
is straightforward.

The class uses the DCHECK_ functions from the `base.log.check` module to do any
argument checks. To disable the checks, the -O flag needs to be set when running
the Python interpreter.
"""
import enum
import pathlib
import shutil
from typing import Optional, Union, List

import kern_comm_lib as kern

__docformat__ = "google"


class FilesystemModes(enum.IntEnum):
  """Enum for file and directory permissions."""
  ALL_RWX = 0o777
  """Full permissions (read, write, execute) for owner, group, and others"""
  ALL_RW = 0o666
  """Read and write permissions for owner, group, and others"""
  OWNER_RWX_OTHERS_RX = 0o755
  """Owner has full permissions, group and others can read/execute"""
  ONLY_OWNER_RWX = 0o700
  """Owner has full permissions, no permissions for group or others"""
  OWNER_RW_OTHERS_R = 0o644
  """Owner can read/write, group and others can only read"""
  ONLY_OWNER_RW = 0o600
  """Owner can read/write, no permissions for group or others"""
  ALL_R = 0o444
  """Read-only permissions for owner, group, and others"""
  ONLY_OWNER_R = 0o400
  """Read-only permissions for owner only"""
  OWNER_RWX_GROUP_RX = 0o750
  """Owner has full permissions, group can read/execute, others have no permissions"""
  OWNER_GROUP_RWX = 0o770
  """Owner and group have full permissions, others have no permissions"""


class KPath:
  """Path class that wraps pathlib.Path and returns status objects instead of raising exceptions."""

  def __init__(
          self,
          a_path: Union[str, pathlib.Path, 'KPath']
  ) -> None:
    """Constructor.

    Args:
      a_path: The path to wrap. Can be a string, pathlib.Path, or another KPath object.
    """
    # <editor-fold desc="Checks">
    kern.DCHECK_NOT_NONE(a_path)
    # </editor-fold>
    # If the path is a string or a KPath object, it has to be converted
    # to a pathlib.Path object because KPath is a wrapper around pathlib.Path.
    if not isinstance(a_path, pathlib.Path):
      self._path: pathlib.Path = pathlib.Path(a_path)
    else:
      self._path: pathlib.Path = a_path

  # <editor-fold desc="Magic methods">
  def __str__(self) -> str:
    """Returns the string representation of the path.

    Returns:
      The string representation of the path.
    """
    return str(self._path)

  def __repr__(self) -> str:
    """Returns the representation of the path.

    Returns:
      The representation of the path.
    """
    return f"KPath({repr(self._path)})"
  # </editor-fold>

  # <editor-fold desc="Getter methods">
  @property
  def name(self) -> str:
    """Gets the name of the file or directory.

    Returns:
      The name of the file or directory
    """
    return self._path.name

  @property
  def parent(self) -> 'KPath':
    """Gets the parent directory as KPath.

    Returns:
      The parent directory as a KPath object.
    """
    return KPath(self._path.parent)

  @property
  def suffix(self) -> str:
    """Gets the file extension.

    Returns:
      The file extension.
    """
    return self._path.suffix

  @property
  def stem(self) -> str:
    """Gets the filename without extension.

    Returns:
      The filename without extension.
    """
    return self._path.stem
  # </editor-fold>

  def exists(self) -> kern.AStatusOrElse[bool]:
    """Checks if the path exists.

    Returns:
      Either True if the path exists or False if it doesn't, otherwise a Status object containing an error status.
    """
    try:
      return self._path.exists()
    except Exception as e:
      return kern.Status.from_exception(e)

  def is_file(self) -> kern.AStatusOrElse[bool]:
    """Checks if the path is a file.

    Returns:
      Either True if the path is a file or False if it doesn't, otherwise a Status object containing an error status.
    """
    try:
      return self._path.is_file()
    except Exception as e:
      return kern.Status.from_exception(e)

  def is_dir(self) -> kern.AStatusOrElse[bool]:
    """Checks if the path is a directory.

    Returns:
      Either True if the path is a directory or False if it doesn't, otherwise a Status object containing an error status.
    """
    try:
      return self._path.is_dir()
    except Exception as e:
      return kern.Status.from_exception(e)

  # Path operations

  def mkdir(
          self,
          mode: int = 0o777,
          parents: bool = False,
          exist_ok: bool = False
  ) -> kern.Status:
    """Creates a directory at this path.

    Args:
      mode (default: 0o777): The mode for the new directory (default is 0o777).
      parents (default: False): If True, create parent directories as needed (default is False).
      exist_ok (default: False): If True, do not raise an error if the directory already exists (default is False).

    Returns:
        A Status object indicating success or failure.
    """
    # <editor-fold desc="Checks">
    kern.DCHECK_NOT_NONE(mode)
    kern.DCHECK_IN_ENUM(mode, FilesystemModes)
    kern.DCHECK_NOT_NONE(parents)
    kern.DCHECK_NOT_NONE(exist_ok)
    # </editor-fold>
    try:
      self._path.mkdir(mode=mode, parents=parents, exist_ok=exist_ok)
      return kern.Status()
    except FileExistsError:
      return kern.Status.from_status_code(
        kern.StatusCode.ALREADY_EXISTS,
        f"Directory already exists: {self._path}"
      )
    except Exception as e:
      return kern.Status.from_exception(e)

  def rmdir(self, recursive: bool = False) -> kern.Status:
    """Removes this directory.

    Args:
        recursive (default: False): If True, removes directory with all its contents. If False, directory must be empty.

    Returns:
      Status object indicating success or failure.
    """
    # <editor-fold desc="Checks">
    kern.DCHECK_NOT_NONE(recursive)
    # </editor-fold>
    try:
      if recursive:
        shutil.rmtree(self._path)
      else:
        self._path.rmdir()
      return kern.Status()
    except FileNotFoundError:
      return kern.status.not_found_error(f"Directory not found: {self._path}")
    except Exception as e:
      return kern.Status.from_exception(e)

  def touch(self, mode: int = 0o666, exist_ok: bool = True) -> kern.Status:
    """Creates a file at this path.

    Args:
        mode: The mode for the new file (default is 0o666).
        exist_ok (default: True): If True, do not raise an error if the file already exists.

    Returns:
      Status object indicating success or failure.
    """
    # <editor-fold desc="Checks">
    kern.DCHECK_NOT_NONE(mode)
    kern.DCHECK_IN_ENUM(mode, FilesystemModes)
    kern.DCHECK_NOT_NONE(exist_ok)
    # </editor-fold>
    try:
      self._path.touch(mode=mode, exist_ok=exist_ok)
      return kern.Status()
    except Exception as e:
      return kern.Status.from_exception(e)

  def unlink(self, missing_ok: bool = False) -> kern.Status:
    """Removes this file or symbolic link.

    Args:
        missing_ok (default: False): If True, do not raise an error if the file does not exist.

    Returns:
      Status object indicating success or failure.
    """
    # <editor-fold desc="Checks">
    kern.DCHECK_NOT_NONE(missing_ok)
    # </editor-fold>
    try:
      self._path.unlink(missing_ok=missing_ok)
      return kern.Status()
    except FileNotFoundError:
      if missing_ok:
        return kern.Status()
      return kern.status.not_found_error(f"File not found: {self._path}")
    except Exception as e:
      return kern.Status.from_exception(e)

  # File content operations

  def read_bytes(self) -> kern.AStatusOrElse[bytes]:
    """Reads bytes from this file.

    Returns:
      Either a bytes object or a Status object containing an error status.
    """
    try:
      return self._path.read_bytes()
    except FileNotFoundError:
      return kern.status.not_found_error(f"File not found: {self._path}")
    except Exception as e:
      return kern.Status.from_exception(e)

  def read_text(self, encoding: str = 'utf-8', errors: Optional[str] = None) -> kern.AStatusOrElse[str]:
    """Reads text from this file.

    Args:
      encoding (default: utf-8): The encoding to use.
      errors (default: None): How to handle encoding errors.

    Returns:
      Either a string of text or a Status object containing an error status.
    """
    # <editor-fold desc="Checks">
    kern.DCHECK_NOT_NONE(encoding)
    kern.DCHECK_NOT_EQ(encoding, "")
    # TODO: Add check for the errors argument! Is an empty string valid?
    # </editor-fold>
    try:
      return self._path.read_text(encoding=encoding, errors=errors)
    except FileNotFoundError:
      return kern.status.not_found_error(f"File not found: {self._path}")
    except Exception as e:
      return kern.Status.from_exception(e)

  def write_bytes(self, data: bytes) -> kern.Status:
    """Writes bytes to this file.

    Args:
      data: The data in bytes to write.

    Returns:
      A Status object indicating success or failure.
    """
    # <editor-fold desc="Checks">
    kern.DCHECK_NOT_NONE(data)
    # </editor-fold>
    try:
      self._path.write_bytes(data)
      return kern.Status()
    except Exception as e:
      return kern.Status.from_exception(e)

  def write_text(self, data: str, encoding: str = 'utf-8', errors: Optional[str] = None) -> kern.Status:
    """Writes text to this file.

    Args:
      data: The data as text to write.
      encoding (default: utf-8): The encoding to use.
      errors (default: None): How to handle encoding errors.

    Returns:
      A Status object indicating success or failure.
    """
    # <editor-fold desc="Checks">
    kern.DCHECK_NOT_NONE(data)
    kern.DCHECK_NOT_NONE(encoding)
    kern.DCHECK_NOT_EQ(encoding, "")
    # TODO: Add check for the errors argument! Is an empty string valid?
    # </editor-fold>
    try:
      self._path.write_text(data, encoding=encoding, errors=errors)
      return kern.Status()
    except Exception as e:
      return kern.Status.from_exception(e)

  # Directory operations

  def iterdir(self) -> kern.AStatusOrElse[List['KPath']]:
    """Iterates over the files in this directory.

    Returns:
      Either a Python list of KPath objects or a Status object containing an error status.
    """
    try:
      return [KPath(path) for path in self._path.iterdir()]
    except FileNotFoundError:
      return kern.status.not_found_error(f"Directory not found: {self._path}")
    except NotADirectoryError:
      return kern.status.invalid_argument_error(f"Not a directory: {self._path}")
    except Exception as e:
      return kern.Status.from_exception(e)
