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
File: base/log/log_severity.py
---------------------------------------------------------------------------

This file declares the log severity level arguments:
- INFO
- WARNING
- ERROR
- FATAL

These should be used with the appropriate LOG function from the base/log/log.py
file.
"""

import enum

__docformat__ = "google"


class LogSeverity(enum.IntEnum):
  """An enumeration representing the severity levels for logging.

  Attributes:
    INFO: Informational messages that highlight the progress of the application.
    WARNING: Potentially harmful situations that should be noted.
    ERROR: Error events that might still allow the application to continue running.
    FATAL: Severe error events that will lead the application to abort.
  """

  INFO = 0
  WARNING = 1
  ERROR = 2
  FATAL = 3


# Convenience aliases for easier access to log severity levels
INFO = LogSeverity.INFO  # Alias for informational messages
WARNING = LogSeverity.WARNING  # Alias for warning messages
ERROR = LogSeverity.ERROR  # Alias for error messages
FATAL = LogSeverity.FATAL  # Alias for fatal error messages
