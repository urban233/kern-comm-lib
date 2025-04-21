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
