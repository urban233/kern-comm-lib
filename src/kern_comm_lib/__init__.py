from typing import TypeVar, Union

from kern_comm_lib.base import status
from kern_comm_lib.base.status import Status
from kern_comm_lib.base.status_or import StatusOr
from kern_comm_lib.base.status_code import StatusCode
from kern_comm_lib.os.platform_vars import IS_WIN
from kern_comm_lib.os.platform_vars import IS_DARWIN
from kern_comm_lib.os.platform_vars import IS_LINUX


T = TypeVar('T')
AStatusOrElse = Union[T, Status]  # Convenient alias for a "value or status" type
