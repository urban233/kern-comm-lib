import pathlib

import kern_comm_lib as kern


def add_to_list(src_list: list, new_item: int) -> kern.Status:
  """Add two numbers."""
  if len(src_list) == 0:
    return kern_comm_lib.base.status.status.invalid_argument_error("List is empty!")
  src_list.append(new_item)
  return kern.Status()


def divide(a: int, b: int) -> kern.AStatusOrElse[float]:
  """Divide two numbers."""
  if b == 0:
    return kern_comm_lib.base.status.status.zero_division_error("Division by zero!")
  return a / b


@kern.use_status
def exists(path: pathlib.Path) -> kern.AStatusOrElse[bool]:
  return path.exists()


def test_decorator() -> None:
  """Test the decorator."""
  tmp_path = pathlib.Path("test.txt")
  tmp_status = kern.StatusOr(bool, exists(tmp_path))
  if tmp_status.ok():
    print(f"Path exists: {tmp_path}")
  else:
    print(f"Error: {tmp_status.status()}")


def test_status_or_init() -> None:
  """Test the initialization of StatusOr class."""
  tmp_list = [1, 2, 3]
  tmp_status: kern.Status = add_to_list(tmp_list, 4)
  assert tmp_status.ok() is True

  tmp_list = []
  tmp_status = add_to_list(tmp_list, 4)
  assert tmp_status.ok() is False

  tmp_number = kern.StatusOr(float, divide(1, 0))
  if tmp_number.ok():
    print(tmp_number.val())
  else:
    err = tmp_number.status()


def test_experiment() -> None:
  """Test to experiment."""
  try:
    pathlib.Path("test.txt").open()
  except Exception as e:
    print(f"Error: {e}")
    tmp_stat = kern.Status.from_exception(e)


def test_status_or_contains_value() -> None:
  """StatusOr should contain a valid value."""
  result = kern.StatusOr(int, 42)
  assert result.ok() is True
  assert result.val() == 42


def test_status_or_contains_error() -> None:
  """StatusOr should contain an error status."""
  error_status = kern_comm_lib.base.status.status.invalid_argument_error("Invalid argument")
  result = kern.StatusOr(int, error_status)
  assert result.ok() is False
  assert result.status() == error_status


def test_status_or_type_mismatch() -> None:
  """StatusOr should raise SystemExit on type mismatch."""
  try:
    kern.StatusOr(int, "string")
  except SystemExit:
    assert True
  else:
    assert False


def test_status_or_ok_status() -> None:
  """StatusOr should return OK status."""
  result = kern.StatusOr(int, 42)
  assert result.status().status_code() == kern.StatusCode.OK


def test_status_or_none_value() -> None:
  """StatusOr should handle None value correctly."""
  result = kern.StatusOr(int, None)
  assert result.ok() is True
  assert result.val() is None
