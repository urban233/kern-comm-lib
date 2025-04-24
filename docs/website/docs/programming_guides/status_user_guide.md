# Status
Kern contains two classes for managing status: `Status` and `StatusOr`.

- `Status`: Holds information about the success or failure of an operation.
- `StatusOr`: Holds either a value or a `Status` object, allowing functions to return both a result and an error status.

## Overview of kern.Status
The Status class is the main class for managing errors in the Kern library. 
It is designed to be used in conjunction with the StatusOr class, which allows functions to return both a value and a status object.

Example:
```python
import kern_comm_lib as kern

def my_function() -> kern.Status: 
  if some_condition:
    return kern.Status()  # Default constructor returns a success status
  else:
    return kern.Status.from_status_code(kern.StatusCode.INTERNAL, "An error occurred")
```

## Checking for errors
To check for errors, you can use the `ok()` method of the `Status` class.

```python
import kern_comm_lib as kern

def my_function() -> kern.Status:
  if some_condition:
    return kern.Status()  # Default constructor returns a success status
  else:
    return kern.Status.from_status_code(kern.StatusCode.INTERNAL, "An error occurred")

def main():
  tmp_status: kern.Status = my_function()
  if not tmp_status.ok():
    print(f"Error: {tmp_status.message()}")
  else:
    print("Success")
```

## Returning a Status or a Value
Suppose a function needs to return a value on success or, alternatively, a `Status` on error. 
The Kern library provides a `kern.StatusOr` class for this purpose.
To access the value, you can use the `val()` method of the `StatusOr` class and
to check for errors, you can use the `ok()` method or access the complete 
status with the method `status()` of the `StatusOr` class.

```python
import kern_comm_lib as kern

def divide(a: int, b: int) -> kern.AStatusOrElse[float]:
  """Divides two numbers."""
  if b == 0:
    return kern.Status.from_status_code(kern.StatusCode.ZERO_DIVISION_ERROR, "Division by zero!")
  return a / b

tmp_nominator = 5
tmp_denominator = 0

tmp_result: kern.StatusOr = kern.StatusOr(float, divide(tmp_nominator, tmp_denominator))
if tmp_result.ok():
  print(f"Division of {tmp_nominator} / {tmp_denominator} is {tmp_result.val()}")
else:
  print(f"Error occured: {tmp_result.status().message()}")
```

## Add Status to existing code
The Kern library provides a decorator called `@use_status` that 
can be applied to existing functions to enable the use of `Status` and 
`StatusOr` for error handling.

```python
import pathlib
import kern_comm_lib as kern

@kern.use_status
def exists(path: pathlib.Path) -> kern.AStatusOrElse[bool]:
  """Checks if a path exists but in an exception-free way."""
  return path.exists()
```
