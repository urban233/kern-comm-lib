from typing import TypeVar, Union

from kern_comm_lib.base import log
from kern_comm_lib.base.log.check import (
    DCHECK,
    DCHECK_EQ,
    DCHECK_IN_ENUM,
    DCHECK_NOT_EQ,
    DCHECK_NOT_NONE,
)
from kern_comm_lib.base.os.platform_vars import IS_DARWIN, IS_LINUX, IS_WIN
from kern_comm_lib.base.status import status
from kern_comm_lib.base.status.status import Status, use_status
from kern_comm_lib.base.status.status_code import StatusCode
from kern_comm_lib.base.status.status_or import StatusOr

T = TypeVar("T")
AStatusOrElse = Union[
    T, Status
]  # Convenient alias for a "value or status" type
