#!/usr/bin/env python3
import os
import subprocess

# Define paths
virtual_env_activate = "source ./langflow_env/bin/activate"
langflow_components_path = "./.langflow/components/custom_components/"

# Set environment variable
os.environ["LANGFLOW_COMPONENTS_PATH"] = langflow_components_path

# Construct command
langflow_command = "python -m langflow --version 1.4.2"

# Combine activation and langflow command
full_command = f"{virtual_env_activate} && {langflow_command}"

# Execute command
try:
    subprocess.run(full_command, shell=True, check=True, executable="/bin/bash")
except subprocess.CalledProcessError as e:
    print(f"Error running Langflow: {e}")
except FileNotFoundError:
    print("Error: /bin/bash not found. Please ensure bash is installed and in your PATH.")
