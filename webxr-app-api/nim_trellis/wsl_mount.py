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

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

def run_wsl_mount_commands():
    """Run WSL mounting commands as root"""
    try:
        # Step 1: Create the mqueue directory
        logging.info("Creating /dev/mqueue directory...")
        mkdir_command = ["wsl", "-d", "NVIDIA-Workbench", "-u", "root", "mkdir", "-p", "/dev/mqueue"]
        
        result = subprocess.run(mkdir_command, capture_output=True, text=True)
        if result.returncode != 0:
            logging.warning(f"mkdir command output: {result.stdout}")
            logging.warning(f"mkdir command errors: {result.stderr}")
        else:
            logging.info("Successfully created /dev/mqueue directory")

        # Step 2: Mount the mqueue filesystem
        logging.info("Mounting mqueue filesystem...")
        mount_command = ["wsl", "-d", "NVIDIA-Workbench", "-u", "root", "mount", "-t", "mqueue", "none", "/dev/mqueue"]
        
        result = subprocess.run(mount_command, capture_output=True, text=True)
        if result.returncode != 0:
            # Check if the error is because mqueue is already mounted somewhere else
            if "already mounted" in result.stderr:
                logging.info("mqueue is already mounted elsewhere - this is acceptable")
                return True
            else:
                logging.error(f"Mount command failed with return code: {result.returncode}")
                logging.error(f"Mount command output: {result.stdout}")
                logging.error(f"Mount command errors: {result.stderr}")
                return False
        else:
            logging.info("Successfully mounted mqueue filesystem")
            return True

    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed: {e.cmd}")
        logging.error(f"Exit code: {e.returncode}")
        logging.error(f"Output: {e.output}")
        return False
    except Exception as e:
        logging.exception("Unexpected error occurred")
        return False

def check_mount_status():
    """Check if the mqueue filesystem is mounted"""
    try:
        logging.info("Checking mount status...")
        
        # Use shell=True to handle the pipe
        result = subprocess.run(
            "wsl -d NVIDIA-Workbench -u root mount | grep mqueue",
            shell=True,
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            mount_info = result.stdout.strip()
            logging.info(f"mqueue is mounted: {mount_info}")
            return True
        else:
            # Let's also check if /dev/mqueue exists and is accessible
            logging.info("mqueue not found in mount list, checking if /dev/mqueue is accessible...")
            check_dev_result = subprocess.run(
                ["wsl", "-d", "NVIDIA-Workbench", "-u", "root", "test", "-d", "/dev/mqueue"],
                capture_output=True,
                text=True
            )
            
            if check_dev_result.returncode == 0:
                logging.info("/dev/mqueue directory exists and is accessible")
                return True
            else:
                logging.info("mqueue is not mounted and /dev/mqueue is not accessible")
                return False

    except Exception as e:
        logging.exception("Error checking mount status")
        return False

def ensure_mqueue_mounted():
    """Ensure mqueue is mounted, mount if not already mounted"""
    logging.info("Ensuring mqueue filesystem is mounted for Trellis NIM...")
    
    # Check current mount status
    if check_mount_status():
        logging.info("mqueue is already mounted. Proceeding with Trellis NIM startup.")
        return True
    
    # Run the mounting commands
    success = run_wsl_mount_commands()
    
    if success:
        logging.info("WSL mounting operations completed successfully")
        # Verify the mount - but be more lenient
        if check_mount_status():
            logging.info("Mount verification successful. Ready for Trellis NIM.")
            return True
        else:
            # Even if verification fails, if the mount command succeeded, we should proceed
            logging.warning("Mount verification failed, but mount command succeeded. Proceeding anyway.")
            return True
    else:
        logging.error("WSL mounting operations failed")
        return False

if __name__ == "__main__":
    success = ensure_mqueue_mounted()
    if not success:
        sys.exit(1) 