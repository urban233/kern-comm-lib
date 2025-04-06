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

from kern_comm_lib.base import status
from kern_comm_lib.base.status import Status
from kern_comm_lib.base.status_or import StatusOr
from kern_comm_lib.base.status_code import StatusCode
from kern_comm_lib.os.platform_vars import IS_WIN
from kern_comm_lib.os.platform_vars import IS_DARWIN
from kern_comm_lib.os.platform_vars import IS_LINUX


T = TypeVar('T')
AStatusOrElse = Union[T, Status]  # Convenient alias for a "value or status" type
