# core/checks/software_updates.py
# Checks for outdated installed software.

from core.utils import run_command, is_windows, is_linux # تأكد من أن is_arch_linux() غير موجودة هنا
import os
import re

class SoftwareUpdatesCheck:
    def __init__(self):
        self.check_name = "Installed Software Updates"
        self.description = "Checks for outdated versions of common software applications that may have known vulnerabilities."
        self.solution = "Keep all installed software updated to their latest versions. Enable automatic updates where possible."
        self.severity = "High"

        self.common_windows_software = {
            "VLC Media Player": {
                "exe_name": "vlc.exe",
                "paths": [
                    os.path.expandvars(r"%PROGRAMFILES%\VideoLAN\VLC"),
                    os.path.expandvars(r"%PROGRAMFILES(X86)%\VideoLAN\VLC")
                ],
                "min_safe_version": "3.0.18" # Simulated minimum safe version
            },
            "7-Zip": {
                "exe_name": "7zFM.exe",
                "paths": [
                    os.path.expandvars(r"%PROGRAMFILES%\7-Zip"),
                    os.path.expandvars(r"%PROGRAMFILES(X86)%\7-Zip")
                ],
                "min_safe_version": "23.01" # Simulated minimum safe version
            },
            "Notepad++": {
                "exe_name": "notepad++.exe",
                "paths": [
                    os.path.expandvars(r"%PROGRAMFILES%\Notepad++"),
                    os.path.expandvars(r"%PROGRAMFILES(X86)%\Notepad++")
                ],
                "min_safe_version": "8.5.4" # Simulated minimum safe version
            }
        }

    def run_check(self):
        if is_windows():
            return self._check_windows_software()
        elif is_linux():
            return self._check_linux_software()
        else:
            return self._create_result(False, "Unsupported OS", "Software update checks are not fully supported on this operating system.", "N/A", "Medium")

    def _check_windows_software(self):
        issues = []
        
        for software_name, details in self.common_windows_software.items():
            found_path = None
            for path in details["paths"]:
                full_path = os.path.join(path, details["exe_name"])
                if os.path.exists(full_path):
                    found_path = full_path
                    break
            
            if found_path:
                command = ["wmic", "datafile", "where", f"name='{found_path.replace('\\', '\\\\')}'", "get", "Version", "/value"]
                stdout, stderr, return_code = run_command(command)
                
                current_version = "N/A"
                if return_code == 0:
                    match = re.search(r"Version=(\d+\.\d+\.\d+(\.\d+)?)", stdout)
                    if match:
                        current_version = match.group(1)
                
                if current_version != "N/A":
                    if self._is_version_older(current_version, details["min_safe_version"]):
                        issues.append(f"{software_name} (Version: {current_version}) is outdated. Minimum recommended: {details['min_safe_version']}.")
                else:
                    issues.append(f"Could not determine version for {software_name} at {found_path}.")
            else:
                pass 

        if issues:
            description = "Outdated software detected:\n" + "\n".join(issues)
            return self._create_result(False, "Outdated Software Found (Windows)", description, self.solution, self.severity)
        else:
            return self._create_result(True, "All Monitored Software Up to Date (Windows)", "No outdated versions of common software were detected.", "N/A", "Low")

    def _check_linux_software(self):
        # On Linux, software updates are typically managed by package managers (apt, dnf, pacman).
        # We need to detect the distribution's package manager and query it.
        
        upgradable_packages = []
        package_manager_found = False

        # Check for apt (Debian/Ubuntu)
        if os.path.exists("/usr/bin/apt"):
            stdout, stderr, return_code = run_command(["sudo", "apt", "list", "--upgradable"])
            if return_code == 0 and "Listing..." not in stdout and stdout.strip():
                upgradable_packages = [line.split('/')[0].strip() for line in stdout.splitlines() if line and 'Listing...' not in line]
            package_manager_found = True
        
        # Check for pacman (Arch Linux)
        elif os.path.exists("/usr/bin/pacman"):
            # pacman -Qu lists foreign and upgradable packages
            # We want only explicitly installed packages and their updates
            stdout, stderr, return_code = run_command(["sudo", "pacman", "-Qu"])
            if return_code == 0 and stdout.strip():
                # Each line is typically "package_name old_version -> new_version"
                upgradable_packages = [line.split(' ')[0].strip() for line in stdout.splitlines() if line.strip()]
            package_manager_found = True
        
        # Add checks for other package managers like dnf (Fedora/RHEL) if needed
        # elif os.path.exists("/usr/bin/dnf"):
        #     stdout, stderr, return_code = run_command(["sudo", "dnf", "check-update"])
        #     if return_code == 100 and stdout.strip(): # return_code 100 means updates are available
        #         upgradable_packages = [line.split(' ')[0].strip() for line in stdout.splitlines() if line and not line.startswith(('Last metadata expiration check:', 'Dependencies resolved.'))]
        #     package_manager_found = True

        if upgradable_packages:
            description = f"System packages require updates. Use your distribution's package manager to update. Packages: {', '.join(upgradable_packages[:5])}..."
            return self._create_result(False, "Pending System Package Updates (Linux)", description, "Run your package manager to update all installed software (e.g., 'sudo pacman -Syu' on Arch, 'sudo apt update && sudo apt upgrade' on Debian/Ubuntu).", self.severity)
        elif package_manager_found:
            return self._create_result(True, "All System Packages Up to Date (Linux)", "No pending updates detected via system package manager.", "N/A", "Low")
        else:
            return self._create_result(True, "Software Update Status (Linux)", "Could not detect a common package manager. Ensure your system's software is regularly updated.", "N/A", "Medium")


    def _is_version_older(self, current, required):
        current_parts = [int(p) for p in current.split('.')]
        required_parts = [int(p) for p in required.split('.')]

        max_len = max(len(current_parts), len(required_parts))
        current_parts += [0] * (max_len - len(current_parts))
        required_parts += [0] * (max_len - len(required_parts))

        for i in range(max_len):
            if current_parts[i] < required_parts[i]:
                return True
            elif current_parts[i] > required_parts[i]:
                return False
        return False # Versions are equal

    def _create_result(self, is_secure, title, description, solution, severity):
        return {
            "check_name": self.check_name,
            "is_secure": is_secure,
            "title": title,
            "description": description,
            "solution": solution,
            "severity": severity
        }
