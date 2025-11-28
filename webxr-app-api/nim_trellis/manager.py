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
import os
import time
from pathlib import Path

from .constants import CONTAINER_NAME


def is_container_running() -> bool:
    """Check if the container is currently running.
    
    Returns True if the container exists and is running, False otherwise.
    """
    try:
        # Prefer running inside WSL if available
        if os.name == "nt":
            cmd = [
                "wsl", "-d", "NVIDIA-Workbench", "/bin/bash", "-lc",
                f"podman ps -a --format '{{{{.Names}}}} {{{{.Status}}}}' | grep '^{CONTAINER_NAME}' || true"
            ]
        else:
            cmd = ["bash", "-lc", f"podman ps -a --format '{{{{.Names}}}} {{{{.Status}}}}' | grep '^{CONTAINER_NAME}' || true"]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=10)
        
        if result.returncode == 0 and result.stdout.strip():
            # Container exists, check if it's running
            status_line = result.stdout.strip()
            if status_line:
                print(f"Container {CONTAINER_NAME} status: {status_line}")
                # Check if status indicates running (not "Exited",  etc.)
                if any(status in status_line.lower() for status in ["up", "running", "starting", "stopping", "created"]):
                    return True
        return False
    except Exception as e:
        print(f"Failed to check container status {CONTAINER_NAME}: {e}")
        return False


def stop_container() -> bool:
    """Stop the TRELLIS NIM podman container if it is running.

    Returns True if the container was successfully stopped or was not running,
    False if the stop operation failed.
    """
    try:
        # First check if container is running
        if not is_container_running():
            print(f"Container {CONTAINER_NAME} is not running")
            return True
        
        print(f"Stopping container {CONTAINER_NAME}...")
        
        # Prefer running inside WSL if available, mirroring run_llama.py behavior
        if os.name == "nt":
            # Use WSL to call podman
            cmd = [
                "wsl", "-d", "NVIDIA-Workbench", "/bin/bash", "-lc",
                f"podman kill {CONTAINER_NAME} || true"
            ]
        else:
            cmd = ["bash", "-lc", f"podman stop {CONTAINER_NAME} || true"]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=30)
        print(result.stdout.strip())
        
        if result.returncode != 0:
            print(f"Warning: podman stop command failed with return code {result.returncode}")
        
        # Wait for container to actually stop
        print("Waiting for container to stop...")
        start_time = time.time()
        timeout = 5  # 5 seconds timeout
        
        while time.time() - start_time < timeout:
            if not is_container_running():
                print(f"✅ Container {CONTAINER_NAME} stopped successfully")
                return True
            print("Container still stopping, waiting...")
            time.sleep(1)
        
        # If container didn't stop gracefully, try force removal
        print(f"Container {CONTAINER_NAME} did not stop within {timeout} seconds, attempting force removal...")
        
        if os.name == "nt":
            force_cmd = [
                "wsl", "-d", "NVIDIA-Workbench", "/bin/bash", "-lc",
                f"podman rm -f {CONTAINER_NAME} || true"
            ]
        else:
            force_cmd = ["bash", "-lc", f"podman rm -f {CONTAINER_NAME} || true"]
        
        force_result = subprocess.run(force_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=30)
        print(force_result.stdout.strip())
        
        if force_result.returncode != 0:
            print(f"Warning: podman rm -f command failed with return code {force_result.returncode}")
        
        # Wait for container to be removed
        print("Waiting for container to be removed...")
        start_time = time.time()
        while time.time() - start_time < timeout:
            if not is_container_running():
                print(f"✅ Container {CONTAINER_NAME} force-removed successfully")
                return True
            print("Container still being removed, waiting...")
            time.sleep(1)
        
        print(f"❌ Timeout: Container {CONTAINER_NAME} could not be stopped or removed within {timeout} seconds")
        return False
        
    except Exception as e:
        print(f"Failed to stop container {CONTAINER_NAME}: {e}")
        return False 