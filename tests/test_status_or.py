import kern_comm_lib as kern


def add_to_list(src_list: list, new_item: int) -> kern.Status:
  """Add two numbers."""
  if len(src_list) == 0:
    return kern.Status.InvalidArgumentError("List is empty!")
  src_list.append(new_item)
  return kern.Status()


def divide(a: int, b: int) -> kern.AStatusOrElse[float]:
  """Divide two numbers."""
  if b == 0:
    return kern.Status.ZeroDivisionError("Division by zero!")
  return a / b


def test_status_or_init():
  """Test the initialization of StatusOr class."""
  tmp_list = [1, 2, 3]
  tmp_status: kern.Status = add_to_list(tmp_list, 4)
  assert tmp_status.ok() is True

  tmp_list = []
  tmp_status: kern.Status = add_to_list(tmp_list, 4)
  assert tmp_status.ok() is False

  tmp_number = kern.StatusOr(float, divide(1, 0))
  if tmp_number.ok():
    print(tmp_number.val)
  else:
    err = tmp_number.status
