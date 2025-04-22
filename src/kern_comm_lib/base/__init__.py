"""Copyright 2025 by Martin Urban.

It is unlawful to modify or remove this copyright notice.
Licensed under the BSD-3-Clause;
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

     https://opensource.org/license/bsd-3-clause

or please see the accompanying LICENSE file for further information.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

---------------------------------------------------------------------------
File: base/__init__.py
---------------------------------------------------------------------------

This file defines the public API of the base package.
"""

from typing import TypeVar, Union

from kern_comm_lib.base.status import status
from kern_comm_lib.base.status.status import Status, use_status
from kern_comm_lib.base.status.status_code import StatusCode
from kern_comm_lib.base.status.status_or import StatusOr

T = TypeVar("T")
AStatusOrElse = Union[
    T, Status
]  # Convenient alias for a "value or status" type

from kern_comm_lib.base.log.check import DCHECK
from kern_comm_lib.base.log.check import DCHECK_EQ
from kern_comm_lib.base.log.check import DCHECK_IN_ENUM
from kern_comm_lib.base.log.check import DCHECK_NOT_EQ
from kern_comm_lib.base.log.check import DCHECK_NOT_NONE
from kern_comm_lib.base.log.check import DCHECK_LESS_THAN
from kern_comm_lib.base.log.check import DCHECK_GREATER_THAN
from kern_comm_lib.base.log.check import DCHECK_IS_TYPE

from kern_comm_lib.base.log.log_severity import LogSeverity
from kern_comm_lib.base.log.log_severity import INFO
from kern_comm_lib.base.log.log_severity import WARNING
from kern_comm_lib.base.log.log_severity import ERROR
from kern_comm_lib.base.log.log_severity import FATAL

from kern_comm_lib.base.log.log_handlers import FileLogHandler
from kern_comm_lib.base.log.log_handlers import ConsoleLogHandler

from kern_comm_lib.base.log.log import init_kern_logging
from kern_comm_lib.base.log.log import close_kern_logging
from kern_comm_lib.base.log.log import init_thread_specific_kern_logging
from kern_comm_lib.base.log.log import close_thread_specific_kern_logging
from kern_comm_lib.base.log.log import LOG
from kern_comm_lib.base.log.log import LOG_INFO
from kern_comm_lib.base.log.log import LOG_WARNING
from kern_comm_lib.base.log.log import LOG_ERROR
from kern_comm_lib.base.log.log import LOG_FATAL
from kern_comm_lib.base.log.log import DLOG
from kern_comm_lib.base.log.log import DLOG_INFO
from kern_comm_lib.base.log.log import DLOG_WARNING
from kern_comm_lib.base.log.log import DLOG_ERROR
from kern_comm_lib.base.log.log import DLOG_FATAL
from kern_comm_lib.base.log.log import TLOG
from kern_comm_lib.base.log.log import TLOG_INFO
from kern_comm_lib.base.log.log import TLOG_WARNING
from kern_comm_lib.base.log.log import TLOG_ERROR
from kern_comm_lib.base.log.log import TLOG_FATAL
from kern_comm_lib.base.log.log import DTLOG
from kern_comm_lib.base.log.log import DTLOG_INFO
from kern_comm_lib.base.log.log import DTLOG_WARNING
from kern_comm_lib.base.log.log import DTLOG_ERROR
from kern_comm_lib.base.log.log import DTLOG_FATAL

from kern_comm_lib.base.os.platform_vars import IS_WIN
from kern_comm_lib.base.os.platform_vars import IS_DARWIN
from kern_comm_lib.base.os.platform_vars import IS_LINUX
