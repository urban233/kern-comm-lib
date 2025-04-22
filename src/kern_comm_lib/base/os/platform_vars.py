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
File: base/os/platform_vars.py
---------------------------------------------------------------------------

This file defines platform-specific variables to determine the current
operating system. It checks the platform at runtime and sets the
three boolean variables:
- IS_WIN: True if the current platform is Windows
- IS_DARWIN: True if the current platform is macOS
- IS_LINUX: True if the current platform is Linux
These variables should be used to write platform-specific code.

"""

import platform

__docformat__ = "google"

import sys


def invalid_platform() -> int:
  """Function that reports that the platform is invalid and returns 1.

  Note:
    This function does not automatically crash the program because this
    creates problems with pythons static type checker. Therefore, the
    function needs to be nested inside exit(). Therefore, the function
    returns a non-zero value.

  Returns:
    1 if the platform is invalid.
  """
  print(f"Invalid platform: {platform.system()}")
  return 1


# <editor-fold desc="Check running OS">
if platform.system() == "Windows":
  IS_WIN = True
  IS_DARWIN = False
  IS_LINUX = False
elif platform.system() == "Darwin":
  IS_WIN = False
  IS_DARWIN = True
  IS_LINUX = False
elif platform.system() == "Linux":
  IS_WIN = False
  IS_DARWIN = False
  IS_LINUX = True
else:
  sys.exit(invalid_platform())
# </editor-fold>
