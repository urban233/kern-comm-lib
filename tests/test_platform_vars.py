import importlib
import platform
from kern_comm_lib.base.os import platform_vars


def test_invalid_platform_returns_non_zero_value():
    assert platform_vars.invalid_platform() == 1


def test_invalid_platform_prints_correct_message(capsys):
    platform_vars.invalid_platform()
    captured = capsys.readouterr()
    assert "Invalid platform:" in captured.out


def test_platform_variables_set_correctly_for_windows(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Windows")
    importlib.reload(platform_vars)
    assert platform_vars.IS_WIN is True
    assert platform_vars.IS_DARWIN is False
    assert platform_vars.IS_LINUX is False


def test_platform_variables_set_correctly_for_darwin(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Darwin")
    importlib.reload(platform_vars)
    assert platform_vars.IS_WIN is False
    assert platform_vars.IS_DARWIN is True
    assert platform_vars.IS_LINUX is False


def test_platform_variables_set_correctly_for_linux(monkeypatch):
    monkeypatch.setattr(platform, "system", lambda: "Linux")
    importlib.reload(platform_vars)
    assert platform_vars.IS_WIN is False
    assert platform_vars.IS_DARWIN is False
    assert platform_vars.IS_LINUX is True
