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
File: examples/logging_example.py
---------------------------------------------------------------------------

This file shows how to use the logging module of the Kern -
Common Python Libraries project.
"""
import kern_comm_lib as kern

if __name__ == '__main__':
  kern.init_kern_logging("example_logging")
  kern.LOG_INFO("This is an info message")
  kern.LOG_WARNING("This is an warning message")
  kern.LOG_ERROR("This is an error message")
  kern.LOG_FATAL("This is a fatal message")
