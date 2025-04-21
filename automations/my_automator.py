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
File: automations/my_automator.py
---------------------------------------------------------------------------

This file defines and executes the automation tree used by the task automator.
"""

import build_kern
import check_code
import format_code
import pytest_kern
import type_check_code

__docformat__ = "google"


AUTOMATION_TREE = {
  "build": {
    "help": "Build targets",
    "subcommands": {
      "kern-package": {
        "help": "Creates the kern Python package.",
        "func": build_kern.build,
      }
    },
  },
  "code": {
    "help": "Commands like checking, formatting, and type checking.",
    "subcommands": {
      "check": {
        "help": "Lints the Python source code using ruff.",
        "func": check_code.check_python_code,
      },
      "format": {
        "help": "Formats the Python source using ruff.",
        "func": format_code.format_python_code,
      },
      "type-check": {
        "help": "Runs the static type checker pyright over the Python source code.",
        "func": type_check_code.type_check_python_code,
      },
    },
  },
  "test": {
    "help": "Test automations",
    "subcommands": {
      "pytest-kern": {
        "help": "Runs all tests for kern using Pytest.",
        "func": pytest_kern.pytest,
      }
    },
  },
}


if __name__ == "__main__":
  from task_automator import automator

  automator.Automator(AUTOMATION_TREE).run()
