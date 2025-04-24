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

tmp_path = kern.filesystem.KPath("file_with_content.txt")
tmp_status: kern.Status = tmp_path.write_bytes(b"Hello, World!")
if not tmp_status.ok():
  print(f"Error occured: {tmp_status.message()}")

tmp_content: kern.StatusOr = kern.StatusOr(bytes, tmp_path.read_bytes())
if tmp_content.ok():
  print(f"File content: {tmp_content.val()}")
else:
  print(f"Error occured: {tmp_content.status().message()}")
```
