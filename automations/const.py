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
File: automations/const.py
---------------------------------------------------------------------------

This file declares a family constants that are supported on multiple
platforms.
"""
import pathlib
import platform
import sys

import toml

__docformat__ = "google"


PROJECT_ROOT_DIR = pathlib.Path(__file__).parent.parent
PYTHON_EXECUTABLE = sys.executable

tmp_pyproject_toml = toml.load(
  pathlib.Path(PROJECT_ROOT_DIR / "pyproject.toml")
)
PROJECT_NAME = tmp_pyproject_toml["project"]["name"]
PROJECT_VERSION = tmp_pyproject_toml["project"]["version"]
PYTHON_VERSION = f"{sys.version_info.major}.{sys.version_info.minor}"


def invalid_platform() -> int:
  """Function that reports that the platform is invalid and returns 1.

  Note:
    This function does not automatically crash the program because this
    creates problems with pythons static type checker. Therefore, the
    function needs to be nested inside exit().
  """
  print(f"Invalid platform: {platform.system()}")
  return 1


# <editor-fold desc="Check running OS">
if platform.system() == "Windows":
  WIN32 = True
  __APPLE__ = False
  __linux__ = False
elif platform.system() == "Darwin":
  WIN32 = False
  __APPLE__ = True
  __linux__ = False
elif platform.system() == "Linux":
  WIN32 = False
  __APPLE__ = False
  __linux__ = True
else:
  sys.exit(invalid_platform())
# </editor-fold>

# <editor-fold desc="OS-specific constants">
if WIN32:
  PYMOL_PACKAGE_DIR = pathlib.Path(
    PROJECT_ROOT_DIR / ".venv/Lib/site-packages/pymol"
  )
  OS_SPECIFIC_DIR = pathlib.Path(PROJECT_ROOT_DIR / "os_specific/windows")
  PIP_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/Scripts/pip.exe")
  POETRY_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/Scripts/poetry.exe")
  PYTEST_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/Scripts/pytest.exe")
  RUFF_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/Scripts/ruff.exe")
  PYINK_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/Scripts/pyink.exe")
  PYRIGHT_FILEPATH = pathlib.Path(
    PROJECT_ROOT_DIR / ".venv/Scripts/pyright.exe"
  )
elif __APPLE__:
  PYMOL_PACKAGE_DIR = pathlib.Path(
    PROJECT_ROOT_DIR / f".venv/lib/python{PYTHON_VERSION}/site-packages/pymol"
  )
  OS_SPECIFIC_DIR = pathlib.Path(PROJECT_ROOT_DIR / "os_specific/macos")
  PIP_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/bin/pip")
  POETRY_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/bin/poetry")
  PYTEST_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/bin/pytest")
  RUFF_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/bin/ruff")
  PYINK_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/bin/pyink")
  PYRIGHT_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/bin/pyright")
elif __linux__:
  PYMOL_PACKAGE_DIR = pathlib.Path(
    PROJECT_ROOT_DIR / f".venv/lib/python{PYTHON_VERSION}/site-packages/pymol"
  )
  OS_SPECIFIC_DIR = pathlib.Path(PROJECT_ROOT_DIR / "os_specific/linux")
  PIP_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/bin/pip")
  POETRY_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/bin/poetry")
  PYTEST_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/bin/pytest")
  RUFF_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/bin/ruff")
  PYINK_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/bin/pyink")
  PYRIGHT_FILEPATH = pathlib.Path(PROJECT_ROOT_DIR / ".venv/bin/pyright")
# </editor-fold>
