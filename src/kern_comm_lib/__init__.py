from kern_comm_lib.base.status import Status
from kern_comm_lib.base.status_or import StatusOr
from kern_comm_lib.base.status_code import StatusCode
from typing import TypeVar, Union

T = TypeVar('T')
AStatusOrElse = Union[T, Status]  # Convenient alias for a "value or status" type
