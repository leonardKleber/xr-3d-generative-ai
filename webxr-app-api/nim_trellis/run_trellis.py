#
# SPDX-FileCopyrightText: Copyright (c) 1993-2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import subprocess
import sys
from pathlib import Path
import logging
from constants import CONTAINER_NAME

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

try:
    # Step 1: Resolve shell script path
    script_dir = Path(__file__).resolve().parent
    ngc_path = script_dir / "ngc.py"
    windows_script_path = script_dir / "start_trellis_container.sh"

    # Convert Windows path to WSL path
    drive_letter = windows_script_path.drive[0].lower()
    wsl_script_path = f"/mnt/{drive_letter}{windows_script_path.as_posix()[2:]}"
    logging.info(f"Resolved WSL script path: {wsl_script_path}")

    # Step 2: Get NGC API Key
    output = subprocess.check_output(
        [sys.executable, ngc_path],
        stderr=subprocess.STDOUT,
        text=True
    )

    # Parse the output to extract the API key (handles warnings or extra text)
    import re
    key_match = re.search(r'nvapi-[a-zA-Z0-9_-]+', output)
    if key_match:
        ngc_api_key = key_match.group(0)
        logging.info("Successfully retrieved and parsed NGC API Key.")
    else:
        logging.error("Could not parse NGC API Key from output.")
        sys.exit(1)

    # Step 3: Prepare environment + command
    bash_command = (
        f"export NGC_API_KEY='{ngc_api_key}' CONTAINER_NAME='{CONTAINER_NAME}' && "
        f"'{wsl_script_path}'"
    )

    # Open log file for writing
    log_file_path = script_dir / "trellis_container.log"
    with open(log_file_path, "w") as log_file:
        logging.info(f"Logging to {log_file_path}")

        # Launch process with Popen to stream output
        process = subprocess.Popen(
            ["wsl", "-d", "NVIDIA-Workbench", "/bin/bash", "-c", bash_command],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        # Stream output line by line
        for line in process.stdout:
            print(line, end='')               # live output to console
            log_file.write(line)              # write to file
            log_file.flush()                  # ensure it's written immediately

        process.wait()  # wait for completion

        if process.returncode != 0:
            logging.error(f"Script executed with code {process.returncode}")
            sys.exit(process.returncode)

    logging.info("Script executed successfully.")

except subprocess.CalledProcessError as e:
    logging.error(f"Command failed: {e.cmd}")
    logging.error(f"Exit code: {e.returncode}")
    logging.error(f"Output: {e.output}")
    sys.exit(e.returncode)

except Exception as e:
    logging.exception("Unexpected error occurred")
    sys.exit(1)