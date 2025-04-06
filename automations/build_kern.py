import subprocess

import const


def build() -> None:
  """Builds the kern package."""
  subprocess.run(
    [const.POETRY_FILEPATH, "build"], cwd=const.PROJECT_ROOT_DIR
  )
