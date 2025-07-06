# core/checks/system_updates.py
# Checks if the system has pending security updates.

from core.utils import run_command, is_linux, is_windows

class SystemUpdatesCheck:
    def __init__(self):
        self.check_name = "System Updates Status"
        self.description = "Checks if your operating system has all the latest security updates installed."
        self.solution = "Run system update commands (e.g., 'sudo apt update && sudo apt upgrade' on Debian/Ubuntu, or use 'pacman -Syu' on Arch Linux). For Windows, check 'Windows Update' settings."
        self.severity = "High" # Default severity

    def run_check(self):
        if is_linux():
            return self._check_linux_updates()
        elif is_windows():
            return self._check_windows_updates()
        else:
            return self._create_result(False, "Unsupported OS", "The current operating system is not supported for this check.", "Install updates manually if available.", "Medium")

    def _check_linux_updates(self):
        # Determine Linux distribution and check for updates accordingly
        
        # Check for Debian/Ubuntu based systems (apt)
        stdout, stderr, return_code = run_command(["which", "apt"])
        if return_code == 0: # apt is available
            # تم إزالة طباعة "Running: sudo apt update..." من هنا
            update_stdout, update_stderr, update_return_code = run_command(["sudo", "apt", "update"], sudo_required=True) 

            # Check for upgradable packages
            stdout, stderr, return_code = run_command(["apt", "list", "--upgradable"])
            
            if "Listing..." in stdout: 
                upgradable_packages = [line for line in stdout.splitlines() if not line.startswith("Listing...") and "upgradable" in line]
            else:
                upgradable_packages = [line for line in stdout.splitlines() if "upgradable" in line]

            if upgradable_packages:
                description = f"Your system has {len(upgradable_packages)} pending updates that may include security patches. Examples: {', '.join(upgradable_packages[:3])}..."
                return self._create_result(False, "Pending system updates", description, self.solution, "High")
            else:
                return self._create_result(True, "System is up to date", "No pending updates found.", "N/A", "Low")
        
        # Check for Arch Linux based systems (pacman)
        stdout, stderr, return_code = run_command(["which", "pacman"])
        if return_code == 0: # pacman is available
            stdout, stderr, return_code = run_command(["pacman", "-Qu"]) # -Qu queries for outdated packages
            if return_code == 0 and not stdout: # No outdated packages
                return self._create_result(True, "System is up to date", "No pending updates found.", "N/A", "Low")
            elif return_code == 0 and stdout: # Outdated packages found
                outdated_packages = stdout.strip().splitlines()
                description = f"Your system has {len(outdated_packages)} pending updates that may include security patches. Examples: {', '.join(outdated_packages[:3])}..."
                return self._create_result(False, "Pending system updates", description, self.solution, "High")
            else:
                return self._create_result(False, "Update check failed", f"Failed to check for updates: {stderr}", self.solution, "Medium")

        # Fallback for other Linux distributions or if package manager not found
        return self._create_result(False, "Linux update check failed", "No supported package manager (apt/pacman) found.", self.solution, "Medium")

    def _check_windows_updates(self):
        # Checking Windows updates programmatically is complex and requires admin privileges.
        # This is a simplified check that tries to use a PowerShell command.
        # This check might not work reliably without full administrative privileges and running the app as administrator.

        # PowerShell command to get pending updates (requires admin)
        powershell_command = [
            "powershell.exe",
            "-Command",
            "Get-WindowsUpdate -ErrorAction SilentlyContinue | Where-Object {$_.IsDownloaded -eq $false -and $_.IsInstalled -eq $false}"
        ]
        
        stdout, stderr, return_code = run_command(powershell_command)
        
        if return_code == 0 and stdout.strip():
            update_lines = [line for line in stdout.splitlines() if line.strip() and "KB" in line]
            if update_lines:
                num_updates = len(update_lines)
                description = f"Your Windows system has {num_updates} pending updates. Please check Windows Update manually."
                return self._create_result(False, "Pending Windows Updates", description, self.solution, "High")
            else:
                return self._create_result(True, "Windows appears up to date (programmatic check)", "No pending updates found using programmatic check.", "N/A", "Low")
        elif return_code != 0:
            error_message = "Programmatic Windows update check failed. Ensure the application is run as administrator and check manually."
            return self._create_result(False, "Windows Update Check Failed", error_message + f" (Error: {stderr[:100]}...)", self.solution, "Medium")
        else:
            return self._create_result(True, "Windows appears up to date", "No pending updates found using programmatic check.", "N/A", "Low")

    def _create_result(self, is_secure, title, description, solution, severity):
        return {
            "check_name": self.check_name,
            "is_secure": is_secure,
            "title": title,
            "description": description,
            "solution": solution,
            "severity": severity
        }
