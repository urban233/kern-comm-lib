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
import platform


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
  exit(invalid_platform())
# </editor-fold>
