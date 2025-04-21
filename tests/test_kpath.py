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
File: tests/test_kpath.py
---------------------------------------------------------------------------

This file defines a number of tests to verify the functionality of the
KPath class.
"""

import kern_comm_lib as kern


def test_path_exists_returns_false_for_nonexistent_path() -> None:
  """Tests that KPath.exists() returns False for a nonexistent file.

  This test verifies that the `exists` method correctly identifies
  that a file does not exist.
  """
  tmp_path = kern.filesystem.KPath("nonexistent_file.txt")
  assert tmp_path.exists() is False


def test_path_is_file_returns_true_for_file() -> None:
  """Tests that KPath.is_file() returns True for an existing file.

  This test creates a file using the `touch` method, verifies that
  it is recognized as a file, and then removes it.
  """
  tmp_path = kern.filesystem.KPath("test_file.txt")
  tmp_status: kern.Status = tmp_path.touch()
  assert tmp_status.ok() is True
  assert tmp_path.is_file() is True
  tmp_status = tmp_path.unlink()
  assert tmp_status.ok() is True


def test_path_is_dir_returns_true_for_directory() -> None:
  """Tests that KPath.is_dir() returns True for an existing directory.

  This test creates a directory using the `mkdir` method, verifies
  that it is recognized as a directory, and then removes it.
  """
  tmp_path = kern.filesystem.KPath("test_dir")
  tmp_status: kern.Status = tmp_path.mkdir()
  assert tmp_status.ok() is True
  assert tmp_path.is_dir() is True
  tmp_status = tmp_path.rmdir()
  assert tmp_status.ok() is True


def test_mkdir_creates_directory_successfully() -> None:
  """Tests that KPath.mkdir() creates a directory successfully.

  This test creates a directory, verifies its existence, and then
  removes it.
  """
  tmp_path = kern.filesystem.KPath("new_dir")
  tmp_status = tmp_path.mkdir()
  assert tmp_status.ok() is True
  assert tmp_path.is_dir() is True
  tmp_status = tmp_path.rmdir()
  assert tmp_status.ok() is True


def test_mkdir_fails_for_existing_directory() -> None:
  """Tests that KPath.mkdir() fails when attempting to create an existing directory.

  This test creates a directory, attempts to create it again with
  `exist_ok=False`, verifies the failure, and then removes the directory.
  """
  tmp_path = kern.filesystem.KPath("existing_dir")
  tmp_status: kern.Status = tmp_path.mkdir()
  assert tmp_status.ok() is True
  tmp_status = tmp_path.mkdir(exist_ok=False)
  assert not tmp_status.ok()
  tmp_status = tmp_path.rmdir()
  assert tmp_status.ok() is True


def test_rmdir_removes_empty_directory() -> None:
  """Tests that KPath.rmdir() removes an empty directory successfully.

  This test creates an empty directory, removes it, and verifies
  that it no longer exists.
  """
  tmp_path = kern.filesystem.KPath("empty_dir")
  tmp_status: kern.Status = tmp_path.mkdir()
  assert tmp_status.ok() is True
  tmp_status = tmp_path.rmdir()
  assert tmp_status.ok()
  assert tmp_path.exists() is False


def test_rmdir_fails_for_nonexistent_directory() -> None:
  """Tests that KPath.rmdir() fails when attempting to remove a nonexistent directory.

  This test verifies that the `rmdir` method returns a failure status
  when the directory does not exist.
  """
  tmp_path = kern.filesystem.KPath("nonexistent_dir")
  tmp_status: kern.Status = tmp_path.rmdir()
  assert tmp_status.ok() is not True


def test_touch_creates_file_successfully() -> None:
  """Tests that KPath.touch() creates a file successfully.

  This test creates a file, verifies its existence, and then removes it.
  """
  tmp_path = kern.filesystem.KPath("new_file.txt")
  tmp_status: kern.Status = tmp_path.touch()
  assert tmp_status.ok() is True
  assert tmp_path.is_file() is True
  tmp_status = tmp_path.unlink()
  assert tmp_status.ok() is True


def test_unlink_removes_file_successfully() -> None:
  """Tests that KPath.unlink() removes a file successfully.

  This test creates a file, removes it, and verifies that it no longer exists.
  """
  tmp_path = kern.filesystem.KPath("file_to_remove.txt")
  tmp_status: kern.Status = tmp_path.touch()
  assert tmp_status.ok() is True
  tmp_status = tmp_path.unlink()
  assert tmp_status.ok() is True
  assert tmp_path.exists() is False


def test_read_bytes_returns_file_content() -> None:
  """Tests that KPath.read_bytes() returns the correct file content.

  This test writes binary content to a file, reads it back, and verifies
  that the content matches. The file is then removed.
  """
  tmp_path = kern.filesystem.KPath("file_with_content.txt")
  tmp_status: kern.Status = tmp_path.write_bytes(b"Hello, World!")
  assert tmp_status.ok() is True
  content: kern.StatusOr = kern.StatusOr(bytes, tmp_path.read_bytes())
  assert content.ok() is True
  assert content.val() == b"Hello, World!"
  tmp_status = tmp_path.unlink()
  assert tmp_status.ok() is True


def test_write_text_creates_file_with_content() -> None:
  """Tests that KPath.write_text() creates a file with the correct content.

  This test writes text content to a file, reads it back, and verifies
  that the content matches. The file is then removed.
  """
  tmp_path = kern.filesystem.KPath("text_file.txt")
  tmp_status: kern.Status = tmp_path.write_text("Sample text")
  assert tmp_status.ok() is True
  content: kern.StatusOr = kern.StatusOr(str, tmp_path.read_text())
  assert content.ok() is True
  assert content.val() == "Sample text"
  tmp_status = tmp_path.unlink()
  assert tmp_status.ok() is True
