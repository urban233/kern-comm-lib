import pathlib
import subprocess

import build_kern
import const


def pytest() -> None:
  build_kern.build()
  subprocess.run(
    [const.PIP_FILEPATH, "install", "--force-reinstall", pathlib.Path(f"./dist/kern_comm_lib-{const.PROJECT_VERSION}-py3-none-any.whl")],
    cwd=const.PROJECT_ROOT_DIR
  )
  subprocess.run(
    [const.PYTEST_FILEPATH],
    cwd=const.PROJECT_ROOT_DIR
  )
  subprocess.run(
    [const.PIP_FILEPATH, "uninstall", "-y", "kern-comm-lib"],
    cwd=const.PROJECT_ROOT_DIR
  )
