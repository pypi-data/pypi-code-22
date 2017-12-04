# Copyright 2017 BBVA
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from deeptracy_core.docker_helpers import run_in_docker

import tempfile


def test_run_in_docker_ok():
    CMD = """sh -c "echo hello > /tmp/$OUTPUT_FILE" """

    with tempfile.TemporaryDirectory(dir="/tmp") as source:
        with run_in_docker(
                "busybox",
                source_code_path=source,
                result_path="/tmp",
                command=CMD) as f:
            assert f == "hello\n"
