import kern_comm_lib as kern
from kern_comm_lib.base.status import status_code


def test_status_code_ok() -> None:
    """StatusCode should return OK for value 0."""
    assert kern.StatusCode.OK == 0


def test_status_code_invalid_argument() -> None:
    """StatusCode should return INVALID_ARGUMENT for value 3."""
    assert kern.StatusCode.INVALID_ARGUMENT == 3


def test_status_code_custom_zero_division() -> None:
    """StatusCode should return ZERO_DIVISION for value -1."""
    assert kern.StatusCode.ZERO_DIVISION == -1


def test_get_status_code_for_known_exception() -> None:
    """get_status_code_for_exception should return correct StatusCode for known exception."""
    assert status_code.get_status_code_for_exception(ValueError()) == kern.StatusCode.VALUE_ERROR


def test_get_status_code_for_unknown_exception() -> None:
    """get_status_code_for_exception should return UNKNOWN for unknown exception."""
    class CustomException(Exception):
        pass
    assert status_code.get_status_code_for_exception(CustomException()) == kern.StatusCode.UNKNOWN


def test_format_exception_traceback_contains_message() -> None:
    """format_exception_traceback should include exception message in the output."""
    try:
        raise ValueError("Test error")
    except ValueError as e:
        formatted_traceback = status_code.format_exception_traceback(e)
        assert "Test error" in formatted_traceback


def test_format_exception_traceback_contains_traceback() -> None:
    """format_exception_traceback should include traceback information in the output."""
    try:
        raise ValueError("Test error")
    except ValueError as e:
        formatted_traceback = status_code.format_exception_traceback(e)
        assert "Traceback" in formatted_traceback
