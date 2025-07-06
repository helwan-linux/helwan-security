# core/utils.py
# Utility functions for the security audit tool.

import subprocess
import platform

def run_command(command, sudo_required=False):
    """
    Runs a shell command and captures its output and return code.
    :param command: A list of strings representing the command and its arguments.
    :param sudo_required: If True, prepends 'sudo' to the command on Linux.
    :return: Tuple of (stdout, stderr, return_code).
    """
    if sudo_required and is_linux():
        command = ["sudo"] + command
    
    try:
        # Use shell=True for windows commands that are not direct executables
        # but rely on shell features (e.g., 'dir', 'type').
        # However, for security and consistency, it's generally better to avoid shell=True
        # unless absolutely necessary. For simple commands like 'apt' or 'pacman',
        # shell=False is preferred.
        process = subprocess.Popen(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,  # Decode stdout/stderr as text
            encoding='utf-8', # Specify encoding
            errors='ignore' # Ignore decoding errors
        )
        stdout, stderr = process.communicate()
        return stdout, stderr, process.returncode
    except FileNotFoundError:
        return "", f"Error: Command '{command[0]}' not found.", 127
    except Exception as e:
        return "", f"An error occurred while running command: {e}", 1

def is_linux():
    """Checks if the current OS is Linux."""
    return platform.system() == "Linux"

def is_windows():
    """Checks if the current OS is Windows."""
    return platform.system() == "Windows"
