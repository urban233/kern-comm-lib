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
File: automations/type_check_code.py
---------------------------------------------------------------------------

This file defines how the static type checker pyright is run over the source
code.
"""
import pathlib
import subprocess

import const

__docformat__ = "google"


def type_check_python_code() -> None:
  """Runs the static type checker pyright over the Python source code."""
  subprocess.check_call(
    [const.PYRIGHT_FILEPATH], cwd=pathlib.Path(const.PROJECT_ROOT_DIR)
  )
