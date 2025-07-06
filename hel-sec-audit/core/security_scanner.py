# core/security_scanner.py
# Orchestrates the execution of various security checks.

from core.checks.system_updates import SystemUpdatesCheck
from core.checks.weak_passwords import WeakPasswordsCheck
from core.checks.open_ports import OpenPortsCheck
from core.checks.firewall_status import FirewallStatusCheck
from core.checks.antivirus_status import AntivirusStatusCheck
from core.checks.browser_security import BrowserSecurityCheck
from core.checks.software_updates import SoftwareUpdatesCheck # <--- استيراد الفحص الجديد
from core.config_manager import ConfigManager

class SecurityScanner:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.all_checks = {
            "System Updates Status": SystemUpdatesCheck(),
            "Weak Password Policies/Usage": WeakPasswordsCheck(),
            "Open Network Ports": OpenPortsCheck(),
            "Firewall Status": FirewallStatusCheck(),
            "Antivirus Status": AntivirusStatusCheck(),
            "Browser Security Settings": BrowserSecurityCheck(),
            "Installed Software Updates": SoftwareUpdatesCheck() # <--- إضافة الفحص الجديد هنا
        }

    def run_all_checks(self, progress_callback=None):
        results = []
        enabled_checks_config = self.config_manager.get_all_check_settings()
        
        checks_to_run = [
            check_instance for check_name, check_instance in self.all_checks.items()
            if enabled_checks_config.get(check_name, True) 
        ]

        total_checks = len(checks_to_run)
        
        for i, check in enumerate(checks_to_run):
            result = check.run_check()
            results.append(result)
            
            if progress_callback:
                progress_percentage = int(((i + 1) / total_checks) * 100)
                progress_callback(progress_percentage, f"Running: {check.check_name}")
        return results
