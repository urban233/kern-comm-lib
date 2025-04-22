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
File: tests/test_platform_vars.py
---------------------------------------------------------------------------

This file defines a number of tests to verify the functionality of the
platform vars module.
"""

import importlib
import platform

from kern_comm_lib.base.os import platform_vars


def test_invalid_platform_returns_non_zero_value() -> None:
  """Tests that invalid_platform() returns the expected error code 1.

  This verifies the function returns a non-zero value to indicate an error condition.
  """
  assert platform_vars.invalid_platform() == 1


def test_invalid_platform_prints_correct_message(capsys) -> None:
  """Tests that invalid_platform() prints the expected error message.

  Args:
      capsys: Pytest fixture to capture stdout and stderr output

  Verifies that the output message contains "Invalid platform:".
  """
  platform_vars.invalid_platform()
  captured = capsys.readouterr()
  assert "Invalid platform:" in captured.out


def test_platform_variables_set_correctly_for_windows(monkeypatch) -> None:
  """Tests platform variables are correctly set when running on Windows.

  Args:
      monkeypatch: Pytest fixture to temporarily modify attributes

  This test mocks the platform.system() to return "Windows" and verifies
  that the platform flags are set appropriately.
  """
  monkeypatch.setattr(platform, "system", lambda: "Windows")
  importlib.reload(platform_vars)
  assert platform_vars.IS_WIN is True
  assert platform_vars.IS_DARWIN is False
  assert platform_vars.IS_LINUX is False


def test_platform_variables_set_correctly_for_darwin(monkeypatch) -> None:
  """Tests platform variables are correctly set when running on Darwin (macOS).

  Args:
      monkeypatch: Pytest fixture to temporarily modify attributes

  This test mocks the platform.system() to return "Darwin" and verifies
  that the platform flags are set appropriately.
  """
  monkeypatch.setattr(platform, "system", lambda: "Darwin")
  importlib.reload(platform_vars)
  assert platform_vars.IS_WIN is False
  assert platform_vars.IS_DARWIN is True
  assert platform_vars.IS_LINUX is False


def test_platform_variables_set_correctly_for_linux(monkeypatch) -> None:
  """Tests platform variables are correctly set when running on Linux.

  Args:
      monkeypatch: Pytest fixture to temporarily modify attributes

  This test mocks the platform.system() to return "Linux" and verifies
  that the platform flags are set appropriately.
  """
  monkeypatch.setattr(platform, "system", lambda: "Linux")
  importlib.reload(platform_vars)
  assert platform_vars.IS_WIN is False
  assert platform_vars.IS_DARWIN is False
  assert platform_vars.IS_LINUX is True
