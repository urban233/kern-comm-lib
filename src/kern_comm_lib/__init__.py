"""
#A* -------------------------------------------------------------------
#B* This file contains source code for running automation tasks related
#-* to the build process of the Kern - Common Python Libraries project.
#C* Copyright 2025 by Martin Urban.
#D* -------------------------------------------------------------------
#E* It is unlawful to modify or remove this copyright notice.
#F* -------------------------------------------------------------------
#G* Please see the accompanying LICENSE file for further information.
#H* -------------------------------------------------------------------
#I* Additional authors of this source file include:
#-*
#-*
#-*
#Z* -------------------------------------------------------------------
"""
from typing import TypeVar, Union

from kern_comm_lib.status import status
from kern_comm_lib.status.status import Status
from kern_comm_lib.status.status import use_status
from kern_comm_lib.status.status_or import StatusOr
from kern_comm_lib.status.status_code import StatusCode
from kern_comm_lib.os.platform_vars import IS_WIN
from kern_comm_lib.os.platform_vars import IS_DARWIN
from kern_comm_lib.os.platform_vars import IS_LINUX
from kern_comm_lib import log
from kern_comm_lib.log.check import DCHECK

T = TypeVar('T')
AStatusOrElse = Union[T, Status]  # Convenient alias for a "value or status" type

__all__ = ["DCHECK"]
