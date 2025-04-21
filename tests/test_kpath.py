import kern_comm_lib as kern


def test_path_exists_returns_false_for_nonexistent_path() -> None:
  tmp_path = kern.filesystem.KPath("nonexistent_file.txt")
  assert tmp_path.exists() is False


def test_path_is_file_returns_true_for_file() -> None:
  tmp_path = kern.filesystem.KPath("test_file.txt")
  tmp_status: kern.Status = tmp_path.touch()
  assert tmp_status.ok() is True
  assert tmp_path.is_file() is True
  tmp_status = tmp_path.unlink()
  assert tmp_status.ok() is True


def test_path_is_dir_returns_true_for_directory() -> None:
  tmp_path = kern.filesystem.KPath("test_dir")
  tmp_status: kern.Status = tmp_path.mkdir()
  assert tmp_status.ok() is True
  assert tmp_path.is_dir() is True
  tmp_status = tmp_path.rmdir()
  assert tmp_status.ok() is True


def test_mkdir_creates_directory_successfully() -> None:
  tmp_path = kern.filesystem.KPath("new_dir")
  tmp_status = tmp_path.mkdir()
  assert tmp_status.ok() is True
  assert tmp_path.is_dir() is True
  tmp_status = tmp_path.rmdir()
  assert tmp_status.ok() is True


def test_mkdir_fails_for_existing_directory() -> None:
  tmp_path = kern.filesystem.KPath("existing_dir")
  tmp_status: kern.Status = tmp_path.mkdir()
  assert tmp_status.ok() is True
  tmp_status = tmp_path.mkdir(exist_ok=False)
  assert not tmp_status.ok()
  tmp_status = tmp_path.rmdir()
  assert tmp_status.ok() is True


def test_rmdir_removes_empty_directory() -> None:
  tmp_path = kern.filesystem.KPath("empty_dir")
  tmp_status: kern.Status = tmp_path.mkdir()
  assert tmp_status.ok() is True
  tmp_status = tmp_path.rmdir()
  assert tmp_status.ok()
  assert tmp_path.exists() is False


def test_rmdir_fails_for_nonexistent_directory() -> None:
  tmp_path = kern.filesystem.KPath("nonexistent_dir")
  tmp_status: kern.Status = tmp_path.rmdir()
  assert tmp_status.ok() is not True


def test_touch_creates_file_successfully() -> None:
  tmp_path = kern.filesystem.KPath("new_file.txt")
  tmp_status: kern.Status = tmp_path.touch()
  assert tmp_status.ok() is True
  assert tmp_path.is_file() is True
  tmp_status = tmp_path.unlink()
  assert tmp_status.ok() is True


def test_unlink_removes_file_successfully() -> None:
  tmp_path = kern.filesystem.KPath("file_to_remove.txt")
  tmp_status: kern.Status = tmp_path.touch()
  assert tmp_status.ok() is True
  tmp_status = tmp_path.unlink()
  assert tmp_status.ok() is True
  assert tmp_path.exists() is False


def test_read_bytes_returns_file_content() -> None:
  tmp_path = kern.filesystem.KPath("file_with_content.txt")
  tmp_status: kern.Status = tmp_path.write_bytes(b"Hello, World!")
  assert tmp_status.ok() is True
  content: kern.StatusOr = kern.StatusOr(bytes, tmp_path.read_bytes())
  assert content.ok() is True
  assert content.val() == b"Hello, World!"
  tmp_status = tmp_path.unlink()
  assert tmp_status.ok() is True


def test_write_text_creates_file_with_content() -> None:
  tmp_path = kern.filesystem.KPath("text_file.txt")
  tmp_status: kern.Status = tmp_path.write_text("Sample text")
  assert tmp_status.ok() is True
  content: kern.StatusOr = kern.StatusOr(str, tmp_path.read_text())
  assert content.ok() is True
  assert content.val() == "Sample text"
  tmp_status = tmp_path.unlink()
  assert tmp_status.ok() is True
