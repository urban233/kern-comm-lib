from typing import TypeVar
from typing import Union

from kern_comm_lib.base.status import status
from kern_comm_lib.base.status.status import Status
from kern_comm_lib.base.status.status import use_status
from kern_comm_lib.base.status.status_code import StatusCode
from kern_comm_lib.base.status.status_or import StatusOr

from kern_comm_lib.base.os.platform_vars import IS_WIN
from kern_comm_lib.base.os.platform_vars import IS_DARWIN
from kern_comm_lib.base.os.platform_vars import IS_LINUX
from kern_comm_lib.base import log
from kern_comm_lib.base.log.check import DCHECK
from kern_comm_lib.base.log.check import DCHECK_EQ
from kern_comm_lib.base.log.check import DCHECK_NOT_EQ
from kern_comm_lib.base.log.check import DCHECK_NOT_NONE
from kern_comm_lib.base.log.check import DCHECK_IN_ENUM

T = TypeVar('T')
AStatusOrElse = Union[T, Status]  # Convenient alias for a "value or status" type
