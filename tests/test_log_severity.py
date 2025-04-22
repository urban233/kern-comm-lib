# Copyright 2025 by Martin Urban.
#
# It is unlawful to modify or remove this copyright notice.
# Licensed under the BSD-3-Clause;
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://opensource.org/license/bsd-3-clause
#
# or please see the accompanying LICENSE file for further information.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS “AS IS” AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
# ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS
# OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN
# IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""
---------------------------------------------------------------------------
File: tests/test_log_severity.py
---------------------------------------------------------------------------

This file defines a number of tests to verify the functionality of the
log severity module.
"""
import enum

import kern_comm_lib as kern


def test_log_severity_has_correct_values() -> None:
  """Tests that the LogSeverity enum has the correct integer values for each severity level.

  Ensures:
    - INFO is 0
    - WARNING is 1
    - ERROR is 2
    - FATAL is 3
  """
  assert kern.LogSeverity.INFO == 0
  assert kern.LogSeverity.WARNING == 1
  assert kern.LogSeverity.ERROR == 2
  assert kern.LogSeverity.FATAL == 3


def test_log_severity_aliases_match_enum_values() -> None:
  """Tests that the convenience aliases for LogSeverity match the corresponding enum values.

  Ensures:
    - INFO alias matches LogSeverity.INFO
    - WARNING alias matches LogSeverity.WARNING
    - ERROR alias matches LogSeverity.ERROR
    - FATAL alias matches LogSeverity.FATAL
  """
  assert kern.INFO == kern.LogSeverity.INFO
  assert kern.WARNING == kern.LogSeverity.WARNING
  assert kern.ERROR == kern.LogSeverity.ERROR
  assert kern.FATAL == kern.LogSeverity.FATAL


def test_log_severity_enum_has_all_levels() -> None:
  """Tests that the LogSeverity enum contains all expected severity levels.

  Ensures:
    - The enum includes INFO, WARNING, ERROR, and FATAL levels.
  """
  assert set(kern.LogSeverity) == {
    kern.LogSeverity.INFO,
    kern.LogSeverity.WARNING,
    kern.LogSeverity.ERROR,
    kern.LogSeverity.FATAL
  }


def test_log_severity_enum_is_instance_of_intenum() -> None:
  """Tests that the LogSeverity enum is a subclass of IntEnum.

  Ensures:
    - LogSeverity inherits from enum.IntEnum.
  """
  assert issubclass(kern.LogSeverity, enum.IntEnum)
