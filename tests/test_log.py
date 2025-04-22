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
File: tests/test_log.py
---------------------------------------------------------------------------

This file defines a number of tests to verify the functionality of the
log module.
"""

import pathlib

import kern_comm_lib as kern


def test_init_default_logger() -> None:
    """Tests the initialization and closure of the default logger.

    This test verifies that the default logger can be initialized and closed
    without any issues.
    """
    assert kern.init_kern_logging("test_init_logger").ok()
    assert kern.close_kern_logging().ok()


def test_init_default_logger_with_file_handler() -> None:
    """Tests the initialization and closure of the default logger with a file handler.

    This test verifies that the default logger can be initialized with a file
    handler, closed properly, and the temporary log directory can be removed.
    """
    tmp_log_path = kern.filesystem.KPath(pathlib.Path(__file__).parent / "logs")
    assert kern.init_kern_logging("test_init_logger", str(tmp_log_path)).ok()
    assert kern.close_kern_logging().ok()
    assert tmp_log_path.rmdir(recursive=True).ok()


def test_init_thread_specific_logger() -> None:
    """Tests the initialization and closure of the thread-specific logger.

    This test ensures that the thread-specific logger can be initialized and
    closed without any issues.
    """
    assert kern.init_thread_specific_kern_logging().ok()
    assert kern.close_thread_specific_kern_logging().ok()


def test_init_thread_specific_logger_with_file_handler() -> None:
    """Tests the initialization and closure of the thread-specific logger with a file handler.

    This test verifies that the thread-specific logger can be initialized with
    a file handler, closed properly, and the temporary log directory can be removed.
    """
    tmp_log_path = kern.filesystem.KPath(pathlib.Path(__file__).parent / "logs")
    assert kern.init_thread_specific_kern_logging(str(tmp_log_path)).ok()
    assert kern.close_thread_specific_kern_logging().ok()
    assert tmp_log_path.rmdir(recursive=True).ok()


def test_log_functions() -> None:
    """Tests the logging functions for different log levels.

    This test ensures that the default logger can log messages at various levels
    (INFO, WARNING, ERROR, FATAL) without any issues.
    """
    assert kern.init_kern_logging("test_log_functions").ok()
    assert kern.LOG(kern.INFO, "This is an info message.").ok()
    assert kern.LOG(kern.WARNING, "This is a warning message.").ok()
    assert kern.LOG(kern.ERROR, "This is an error message.").ok()
    assert kern.LOG(kern.FATAL, "This is a fatal message.").ok()


def test_dlog_functions() -> None:
    """Tests the debug logging functions for different log levels.

    This test ensures that the default logger can log debug messages at various
    levels (INFO, WARNING, ERROR, FATAL) without any issues.
    """
    assert kern.init_kern_logging("test_dlog_functions").ok()
    assert kern.DLOG(kern.INFO, "This is an info debug message.") is None
    assert kern.DLOG(kern.WARNING, "This is a warning debug message.") is None
    assert kern.DLOG(kern.ERROR, "This is an error debug message.") is None
    assert kern.DLOG(kern.FATAL, "This is a fatal debug message.") is None


def test_tlog_functions() -> None:
    """Tests the thread-specific logging functions for different log levels.

    This test ensures that the thread-specific logger can log messages at various
    levels (INFO, WARNING, ERROR, FATAL) without any issues.
    """
    assert kern.init_thread_specific_kern_logging().ok()
    assert kern.TLOG(kern.INFO, "This is an info thread-specific message.").ok()
    assert kern.TLOG(kern.WARNING, "This is a warning thread-specific message.").ok()
    assert kern.TLOG(kern.ERROR, "This is an error thread-specific message.").ok()
    assert kern.TLOG(kern.FATAL, "This is a fatal thread-specific message.").ok()


def test_dtlog_functions() -> None:
    """Tests the thread-specific debug logging functions for different log levels.

    This test ensures that the thread-specific logger can log debug messages at
    various levels (INFO, WARNING, ERROR, FATAL) without any issues.
    """
    assert kern.init_thread_specific_kern_logging().ok()
    assert kern.DTLOG(kern.INFO, "This is an info debug message.") is None
    assert kern.DTLOG(kern.WARNING, "This is a warning debug message.") is None
    assert kern.DTLOG(kern.ERROR, "This is an error debug message.") is None
    assert kern.DTLOG(kern.FATAL, "This is a fatal debug message.") is None
