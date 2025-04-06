# Common commands
Here is a list of common commands that are used in the Kern library.

## Ruff
```shell
ruff --config .\pyproject.toml format .\src\kern_comm_lib\
```

```shell
ruff --config .\pyproject.toml check .\src\kern_comm_lib\ --fix
```

## Poetry (and pip)
```shell
poetry build 
```

```shell
pip install .\dist\kern_comm_lib-0.0.2-py3-none-any.whl --force-reinstall
```

```shell
pip uninstall kern-comm-lib
```

## Pytest
```shell
pytest
```