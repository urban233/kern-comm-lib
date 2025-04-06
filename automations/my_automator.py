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
import build_kern
import pytest_kern


AUTOMATION_TREE = {
  # "setup": {
  #   "help": "Setup automations",
  #   "subcommands": {
  #     "dev-env": {
  #       "help": "Sets up the development environment",
  #       "func": setup_dev_env.setup
  #     },
  #     "cpp-exe-env": {
  #       "help": "Sets up the C++ execution environment",
  #       "func": setup_cpp_exe_env.setup
  #     }
  #   }
  # },
  "build": {
    "help": "Build targets",
    "subcommands": {
      "kern-package": {
        "help": "Creates the kern Python package.",
        "func": build_kern.build
      }
    },
  },
  "test": {
    "help": "Test automations",
    "subcommands": {
      "pytest-kern": {
        "help": "Runs all tests for kern using Pytest.",
        "func": pytest_kern.pytest
      }
    }
  }
}


if __name__ == "__main__":
  from task_automator import automator
  automator.Automator(AUTOMATION_TREE).run()
