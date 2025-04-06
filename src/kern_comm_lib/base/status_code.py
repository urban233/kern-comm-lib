import enum


class StatusCode(enum.IntEnum):
  """Status codes for StatusOr and Status classes.

  Includes Google canonical error codes (0-16), custom codes, and Python standard
  error codes (100+).
  """

  # <editor-fold desc="Google canonical error codes">
  OK = 0
  CANCELLED = 1
  UNKNOWN = 2
  INVALID_ARGUMENT = 3
  DEADLINE_EXCEEDED = 4
  NOT_FOUND = 5
  ALREADY_EXISTS = 6
  PERMISSION_DENIED = 7
  RESOURCE_EXHAUSTED = 8
  FAILED_PRECONDITION = 9
  ABORTED = 10
  OUT_OF_RANGE = 11
  UNIMPLEMENTED = 12
  INTERNAL = 13
  UNAVAILABLE = 14
  DATA_LOSS = 15
  UNAUTHENTICATED = 16
  # </editor-fold>
  # <editor-fold desc="Custom error codes">
  ZERO_DIVISION = -1
  # </editor-fold>
  # <editor-fold desc="Python standard error codes (100+)">
  ARITHMETIC_ERROR = 100
  ASSERTION_ERROR = 101
  ATTRIBUTE_ERROR = 102
  BLOCKING_IO_ERROR = 103
  BROKEN_PIPE_ERROR = 104
  BUFFER_ERROR = 105
  CHILD_PROCESS_ERROR = 106
  CONNECTION_ABORTED_ERROR = 107
  CONNECTION_ERROR = 108
  CONNECTION_REFUSED_ERROR = 109
  CONNECTION_RESET_ERROR = 110
  EOF_ERROR = 111
  FILE_EXISTS_ERROR = 112
  FILE_NOT_FOUND_ERROR = 113
  FLOATING_POINT_ERROR = 114
  GENERATOR_EXIT = 115
  IMPORT_ERROR = 116
  INDENTATION_ERROR = 117
  INDEX_ERROR = 118
  INTERRUPTED_ERROR = 119
  IS_A_DIRECTORY_ERROR = 120
  KEY_ERROR = 121
  KEYBOARD_INTERRUPT = 122
  LOOKUP_ERROR = 123
  MEMORY_ERROR = 124
  MODULE_NOT_FOUND_ERROR = 125
  NAME_ERROR = 126
  NOT_A_DIRECTORY_ERROR = 127
  NOT_IMPLEMENTED_ERROR = 128
  OS_ERROR = 129
  OVERFLOW_ERROR = 130
  PERMISSION_ERROR = 131
  PROCESS_LOOKUP_ERROR = 132
  RECURSION_ERROR = 133
  REFERENCE_ERROR = 134
  RUNTIME_ERROR = 135
  STOP_ASYNC_ITERATION = 136
  STOP_ITERATION = 137
  SYNTAX_ERROR = 138
  SYSTEM_ERROR = 139
  SYSTEM_EXIT = 140
  TAB_ERROR = 141
  TIMEOUT_ERROR = 142
  TYPE_ERROR = 143
  UNBOUND_LOCAL_ERROR = 144
  UNICODE_DECODE_ERROR = 145
  UNICODE_ENCODE_ERROR = 146
  UNICODE_ERROR = 147
  UNICODE_TRANSLATE_ERROR = 148
  VALUE_ERROR = 149
  ZERO_DIVISION_ERROR = 150
  # </editor-fold>


# Exception to StatusCode mapping
EXCEPTION_TO_STATUS_CODE = {
  ArithmeticError: StatusCode.ARITHMETIC_ERROR,
  AssertionError: StatusCode.ASSERTION_ERROR,
  AttributeError: StatusCode.ATTRIBUTE_ERROR,
  BlockingIOError: StatusCode.BLOCKING_IO_ERROR,
  BrokenPipeError: StatusCode.BROKEN_PIPE_ERROR,
  BufferError: StatusCode.BUFFER_ERROR,
  ChildProcessError: StatusCode.CHILD_PROCESS_ERROR,
  ConnectionAbortedError: StatusCode.CONNECTION_ABORTED_ERROR,
  ConnectionError: StatusCode.CONNECTION_ERROR,
  ConnectionRefusedError: StatusCode.CONNECTION_REFUSED_ERROR,
  ConnectionResetError: StatusCode.CONNECTION_RESET_ERROR,
  EOFError: StatusCode.EOF_ERROR,
  FileExistsError: StatusCode.FILE_EXISTS_ERROR,
  FileNotFoundError: StatusCode.FILE_NOT_FOUND_ERROR,
  FloatingPointError: StatusCode.FLOATING_POINT_ERROR,
  GeneratorExit: StatusCode.GENERATOR_EXIT,
  ImportError: StatusCode.IMPORT_ERROR,
  IndentationError: StatusCode.INDENTATION_ERROR,
  IndexError: StatusCode.INDEX_ERROR,
  InterruptedError: StatusCode.INTERRUPTED_ERROR,
  IsADirectoryError: StatusCode.IS_A_DIRECTORY_ERROR,
  KeyError: StatusCode.KEY_ERROR,
  KeyboardInterrupt: StatusCode.KEYBOARD_INTERRUPT,
  LookupError: StatusCode.LOOKUP_ERROR,
  MemoryError: StatusCode.MEMORY_ERROR,
  ModuleNotFoundError: StatusCode.MODULE_NOT_FOUND_ERROR,
  NameError: StatusCode.NAME_ERROR,
  NotADirectoryError: StatusCode.NOT_A_DIRECTORY_ERROR,
  NotImplementedError: StatusCode.NOT_IMPLEMENTED_ERROR,
  OSError: StatusCode.OS_ERROR,
  OverflowError: StatusCode.OVERFLOW_ERROR,
  PermissionError: StatusCode.PERMISSION_ERROR,
  ProcessLookupError: StatusCode.PROCESS_LOOKUP_ERROR,
  RecursionError: StatusCode.RECURSION_ERROR,
  ReferenceError: StatusCode.REFERENCE_ERROR,
  RuntimeError: StatusCode.RUNTIME_ERROR,
  StopAsyncIteration: StatusCode.STOP_ASYNC_ITERATION,
  StopIteration: StatusCode.STOP_ITERATION,
  SyntaxError: StatusCode.SYNTAX_ERROR,
  SystemError: StatusCode.SYSTEM_ERROR,
  SystemExit: StatusCode.SYSTEM_EXIT,
  TabError: StatusCode.TAB_ERROR,
  TimeoutError: StatusCode.TIMEOUT_ERROR,
  TypeError: StatusCode.TYPE_ERROR,
  UnboundLocalError: StatusCode.UNBOUND_LOCAL_ERROR,
  UnicodeDecodeError: StatusCode.UNICODE_DECODE_ERROR,
  UnicodeEncodeError: StatusCode.UNICODE_ENCODE_ERROR,
  UnicodeError: StatusCode.UNICODE_ERROR,
  UnicodeTranslateError: StatusCode.UNICODE_TRANSLATE_ERROR,
  ValueError: StatusCode.VALUE_ERROR,
  ZeroDivisionError: StatusCode.ZERO_DIVISION_ERROR,
}


def get_status_code_for_exception(exception: Exception) -> StatusCode:
  """Maps a Python exception to the appropriate StatusCode.

  Args:
      exception: The Python exception to map

  Returns:
      The corresponding StatusCode enum value
  """
  exception_type = type(exception)

  # Direct type lookup
  if exception_type in EXCEPTION_TO_STATUS_CODE:
    return EXCEPTION_TO_STATUS_CODE[exception_type]

  # Try to find a parent exception class
  for exc_type, code in EXCEPTION_TO_STATUS_CODE.items():
    if isinstance(exception, exc_type):
      return code

  # Default fallback
  return StatusCode.UNKNOWN


def format_exception_traceback(exception: Exception) -> str:
  """Formats an exception's traceback into a human-readable string.

  Args:
      exception: The Python exception to format

  Returns:
      A formatted string containing the traceback information
  """
  import traceback

  return "".join(
    traceback.format_exception(
      type(exception), exception, exception.__traceback__
    )
  )
