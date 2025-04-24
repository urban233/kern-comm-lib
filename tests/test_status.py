import pathlib
import kern_comm_lib as kern


@kern.use_status
def exists(path: pathlib.Path) -> kern.AStatusOrElse[bool]:
  """Checks if a path exists but in an exception-free way."""
  return path.exists()


def test_decorator() -> None:
  """Tests the decorator."""
  tmp_path = pathlib.Path("test.txt")
  tmp_status = kern.StatusOr(bool, exists(tmp_path))
  if tmp_status.ok():
    print(f"Path exists: {tmp_path}")
  else:
    print(f"Error: {tmp_status.status()}")
