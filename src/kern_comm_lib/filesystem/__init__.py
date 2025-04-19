import os
import errno
from typing import List, Union, Optional, TypeVar, BinaryIO, TextIO, Tuple

import pathlib
import kern_comm_lib as kern
from kern_comm_lib.status import status_code

T = TypeVar('T')


class StatusPath:
  """Exception-free wrapper around pathlib.Path using Status and StatusOr."""

  def __init__(self, path: Union[str, pathlib.Path, 'StatusPath']) -> None:
    """Initialize with a path string or Path object."""
    if isinstance(path, StatusPath):
      self._path = path._path
    else:
      self._path = pathlib.Path(path)

  @property
  def path(self) -> pathlib.Path:
    """Get the underlying pathlib.Path object."""
    return self._path

  def __str__(self) -> str:
    return str(self._path)

  def __repr__(self) -> str:
    return f"StatusPath('{self._path}')"

  # Path properties

  @property
  def name(self) -> str:
    """The name of the final path component."""
    return self._path.name

  @property
  def stem(self) -> str:
    """The final path component without its suffix."""
    return self._path.stem

  @property
  def suffix(self) -> str:
    """The file extension of the final component."""
    return self._path.suffix

  @property
  def suffixes(self) -> List[str]:
    """A list of the path's file extensions."""
    return self._path.suffixes

  @property
  def parts(self) -> Tuple[str, ...]:
    """A tuple giving access to the path's components."""
    return self._path.parts

  def parent(self) -> 'StatusPath':
    """The path's parent directory."""
    return StatusPath(self._path.parent)

  def parents(self) -> List['StatusPath']:
    """An immutable sequence of this path's parents."""
    return [StatusPath(parent) for parent in self._path.parents]

  # Path operations

  def joinpath(self, *paths: Union[str, pathlib.Path, 'StatusPath']) -> 'StatusPath':
    """Combine this path with one or more paths."""
    try:
      joined_paths = [p._path if isinstance(p, StatusPath) else p for p in paths]
      return StatusPath(self._path.joinpath(*joined_paths))
    except Exception as e:
      return kern.Status.from_exception(e)

  def with_name(self, name: str) -> kern.AStatusOrElse['StatusPath']:
    """Return a new path with the name changed."""
    try:
      return StatusPath(self._path.with_name(name))
    except Exception as e:
      return kern.Status.from_exception(e)

  def with_suffix(self, suffix: str) -> kern.AStatusOrElse['StatusPath']:
    """Return a new path with the suffix changed."""
    try:
      return StatusPath(self._path.with_suffix(suffix))
    except Exception as e:
      return kern.Status.from_exception(e)

  def is_absolute(self) -> bool:
    """Check if the path is absolute."""
    return self._path.is_absolute()

  def is_reserved(self) -> bool:
    """Check if the path is a reserved path on Windows."""
    return self._path.is_reserved()

  def absolute(self) -> kern.AStatusOrElse['StatusPath']:
    """Return the absolute path."""
    try:
      return StatusPath(self._path.absolute())
    except Exception as e:
      return kern.Status.from_exception(e)

  def resolve(self, strict: bool = False) -> kern.AStatusOrElse['StatusPath']:
    """Return the canonical path, resolving symlinks."""
    try:
      return StatusPath(self._path.resolve(strict=strict))
    except Exception as e:
      return kern.Status.from_exception(e)

  def relative_to(self, *other: Union[str, pathlib.Path, 'StatusPath']) -> kern.AStatusOrElse['StatusPath']:
    """Return the relative path to another path."""
    try:
      other_paths = [p._path if isinstance(p, StatusPath) else p for p in other]
      return StatusPath(self._path.relative_to(*other_paths))
    except Exception as e:
      return kern.Status.from_exception(e)

  # File system operations

  def exists(self) -> kern.AStatusOrElse[bool]:
    """Return True if the path exists."""
    try:
      return self._path.exists()
    except Exception as e:
      return kern.Status.from_exception(e)

  def is_dir(self) -> kern.AStatusOrElse[bool]:
    """Return True if the path is a directory."""
    try:
      return self._path.is_dir()
    except Exception as e:
      return kern.Status.from_exception(e)

  def is_file(self) -> kern.AStatusOrElse[bool]:
    """Return True if the path is a regular file."""
    try:
      return self._path.is_file()
    except Exception as e:
      return kern.Status.from_exception(e)

  def is_symlink(self) -> kern.AStatusOrElse[bool]:
    """Return True if the path is a symbolic link."""
    try:
      return self._path.is_symlink()
    except Exception as e:
      return kern.Status.from_exception(e)

  def stat(self, follow_symlinks: bool = True) -> kern.AStatusOrElse[os.stat_result]:
    """Return the result of os.stat() on this path."""
    try:
      return self._path.stat(follow_symlinks=follow_symlinks)
    except Exception as e:
      return kern.Status.from_exception(e)

  def chmod(self, mode: int) -> kern.Status:
    """Change file permissions."""
    try:
      self._path.chmod(mode)
      return kern.Status()
    except Exception as e:
      return kern.Status.from_exception(e)

  def lchmod(self, mode: int) -> kern.Status:
    """Change the permissions of a file, without following symbolic links."""
    try:
      self._path.lchmod(mode)
      return kern.Status()
    except Exception as e:
      return kern.Status.from_exception(e)

  def mkdir(self, mode: int = 0o777, parents: bool = False, exist_ok: bool = False) -> kern.Status:
    """Create a new directory at this path."""
    try:
      self._path.mkdir(mode=mode, parents=parents, exist_ok=exist_ok)
      return kern.Status()
    except FileExistsError:
      return kern_comm_lib.status.status.custom_error(
        status_code.StatusCode.ALREADY_EXISTS,
        f"Directory already exists: {self._path}"
      )
    except Exception as e:
      return kern.Status.from_exception(e)

  def rmdir(self) -> kern.Status:
    """Remove this directory."""
    try:
      self._path.rmdir()
      return kern.Status()
    except FileNotFoundError:
      return kern_comm_lib.status.status.not_found_error(f"Directory not found: {self._path}")
    except OSError as e:
      if e.errno == errno.ENOTEMPTY:
        return kern_comm_lib.status.status.custom_error(
          status_code.StatusCode.FAILED_PRECONDITION,
          f"Directory not empty: {self._path}"
        )
      return kern.Status.from_exception(e)
    except Exception as e:
      return kern.Status.from_exception(e)

  def touch(self, mode: int = 0o666, exist_ok: bool = True) -> kern.Status:
    """Create file at this path."""
    try:
      self._path.touch(mode=mode, exist_ok=exist_ok)
      return kern.Status()
    except Exception as e:
      return kern.Status.from_exception(e)

  def unlink(self, missing_ok: bool = False) -> kern.Status:
    """Remove this file or symbolic link."""
    try:
      self._path.unlink(missing_ok=missing_ok)
      return kern.Status()
    except FileNotFoundError:
      if missing_ok:
        return kern.Status()
      return kern_comm_lib.status.status.not_found_error(f"File not found: {self._path}")
    except Exception as e:
      return kern.Status.from_exception(e)

  def rename(self, target: Union[str, pathlib.Path, 'StatusPath']) -> kern.Status:
    """Rename this file or directory."""
    try:
      target_path = target._path if isinstance(target, StatusPath) else target
      self._path.rename(target_path)
      return kern.Status()
    except FileExistsError:
      return kern_comm_lib.status.status.custom_error(
        status_code.StatusCode.ALREADY_EXISTS,
        f"Target already exists: {target}"
      )
    except Exception as e:
      return kern.Status.from_exception(e)

  def replace(self, target: Union[str, pathlib.Path, 'StatusPath']) -> kern.Status:
    """Rename this file or directory, replacing the target if it exists."""
    try:
      target_path = target._path if isinstance(target, StatusPath) else target
      self._path.replace(target_path)
      return kern.Status()
    except Exception as e:
      return kern.Status.from_exception(e)

  def symlink_to(self, target: Union[str, pathlib.Path, 'StatusPath'],
                 target_is_directory: bool = False) -> kern.Status:
    """Create a symbolic link to a target."""
    try:
      target_path = target._path if isinstance(target, StatusPath) else target
      self._path.symlink_to(target_path, target_is_directory=target_is_directory)
      return kern.Status()
    except Exception as e:
      return kern.Status.from_exception(e)

  # File content operations

  def open(self, mode: str = 'r', buffering: int = -1,
           encoding: Optional[str] = None, errors: Optional[str] = None,
           newline: Optional[str] = None) -> kern.AStatusOrElse[Union[TextIO, BinaryIO]]:
    """Open the file pointed to by this path."""
    try:
      return self._path.open(mode=mode, buffering=buffering,
                             encoding=encoding, errors=errors, newline=newline)
    except Exception as e:
      return kern.Status.from_exception(e)

  def read_bytes(self) -> kern.AStatusOrElse[bytes]:
    """Read bytes from this file."""
    try:
      return self._path.read_bytes()
    except FileNotFoundError:
      return kern_comm_lib.status.status.not_found_error(f"File not found: {self._path}")
    except Exception as e:
      return kern.Status.from_exception(e)

  def read_text(self, encoding: str = 'utf-8', errors: Optional[str] = None) -> kern.AStatusOrElse[str]:
    """Read text from this file."""
    try:
      return self._path.read_text(encoding=encoding, errors=errors)
    except FileNotFoundError:
      return kern_comm_lib.status.status.not_found_error(f"File not found: {self._path}")
    except Exception as e:
      return kern.Status.from_exception(e)

  def write_bytes(self, data: bytes) -> kern.Status:
    """Write bytes to this file."""
    try:
      self._path.write_bytes(data)
      return kern.Status()
    except Exception as e:
      return kern.Status.from_exception(e)

  def write_text(self, data: str, encoding: str = 'utf-8', errors: Optional[str] = None) -> kern.Status:
    """Write text to this file."""
    try:
      self._path.write_text(data, encoding=encoding, errors=errors)
      return kern.Status()
    except Exception as e:
      return kern.Status.from_exception(e)

  # Directory content operations

  def iterdir(self) -> kern.AStatusOrElse[List['StatusPath']]:
    """Iterate over the files in this directory."""
    try:
      return [StatusPath(path) for path in self._path.iterdir()]
    except FileNotFoundError:
      return kern_comm_lib.status.status.not_found_error(f"Directory not found: {self._path}")
    except NotADirectoryError:
      return kern_comm_lib.status.status.invalid_argument_error(f"Not a directory: {self._path}")
    except Exception as e:
      return kern.Status.from_exception(e)

  def glob(self, pattern: str) -> kern.AStatusOrElse[List['StatusPath']]:
    """Glob the given relative pattern in the directory."""
    try:
      return [StatusPath(path) for path in self._path.glob(pattern)]
    except Exception as e:
      return kern.Status.from_exception(e)

  def rglob(self, pattern: str) -> kern.AStatusOrElse[List['StatusPath']]:
    """Recursively glob the given relative pattern in the directory."""
    try:
      return [StatusPath(path) for path in self._path.rglob(pattern)]
    except Exception as e:
      return kern.Status.from_exception(e)

  # Static methods

  @staticmethod
  def cwd() -> kern.AStatusOrElse['StatusPath']:
    """Return a new path pointing to the current working directory."""
    try:
      return StatusPath(pathlib.Path.cwd())
    except Exception as e:
      return kern.Status.from_exception(e)

  @staticmethod
  def home() -> kern.AStatusOrElse['StatusPath']:
    """Return a new path pointing to the user's home directory."""
    try:
      return StatusPath(pathlib.Path.home())
    except Exception as e:
      return kern.Status.from_exception(e)
