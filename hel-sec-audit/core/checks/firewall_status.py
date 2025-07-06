# core/checks/firewall_status.py
# Checks the status of the system's firewall.

from core.utils import run_command, is_linux, is_windows

class FirewallStatusCheck:
    def __init__(self):
        self.check_name = "Firewall Status"
        self.description = "Verifies if the system's firewall is active and properly configured to protect against unauthorized access."
        self.solution = "Ensure your system's firewall (e.g., Windows Defender Firewall, UFW, Firewalld) is enabled and configured to block unnecessary incoming connections."
        self.severity = "High"

    def run_check(self):
        if is_linux():
            return self._check_linux_firewall()
        elif is_windows():
            return self._check_windows_firewall()
        else:
            return self._create_result(False, "Unsupported OS", "The current operating system is not supported for this check.", "N/A", "Medium")

    def _check_linux_firewall(self):
        # Try checking UFW first (Ubuntu/Debian)
        # محاولة التحقق من UFW أولاً (أوبونتو/دبيان)
        stdout, stderr, return_code = run_command(["sudo", "ufw", "status"])
        if return_code == 0 and "Status: active" in stdout:
            return self._create_result(True, "UFW is active", "Uncomplicated Firewall (UFW) is enabled and providing protection.", "N/A", "Low")
        elif return_code == 0 and "Status: inactive" in stdout:
            return self._create_result(False, "UFW is inactive", "Uncomplicated Firewall (UFW) is disabled. Your system is exposed.", "Enable UFW: 'sudo ufw enable'", "High")

        # If UFW not found or inactive, try Firewalld (Fedora/CentOS/RHEL)
        # إذا لم يتم العثور على UFW أو كان غير نشط، جرب Firewalld
        stdout, stderr, return_code = run_command(["sudo", "systemctl", "is-active", "firewalld"])
        if return_code == 0 and "active" in stdout:
            return self._create_result(True, "Firewalld is active", "Firewalld is enabled and providing protection.", "N/A", "Low")
        elif return_code == 0 and "inactive" in stdout:
            return self._create_result(False, "Firewalld is inactive", "Firewalld is disabled. Your system is exposed.", "Enable Firewalld: 'sudo systemctl start firewalld && sudo systemctl enable firewalld'", "High")
        
        # Fallback if no known firewall detected or active
        # في حالة عدم اكتشاف جدار حماية معروف أو نشط
        return self._create_result(False, "Linux Firewall Status Unknown/Inactive", "Could not determine status of a common Linux firewall (UFW/Firewalld) or it is inactive.", self.solution, "Medium")


    def _check_windows_firewall(self):
        # Use 'netsh advfirewall show allprofiles' to check Windows Defender Firewall status
        # استخدام 'netsh advfirewall show allprofiles' للتحقق من حالة Windows Defender Firewall
        command = ["netsh", "advfirewall", "show", "allprofiles"]
        stdout, stderr, return_code = run_command(command)

        if return_code != 0:
            return self._create_result(False, "Windows Firewall Check Failed", "Could not check Windows Firewall status (possibly due to insufficient permissions). Please run as administrator.", self.solution, "Medium")

        is_private_active = False
        is_public_active = False
        is_domain_active = False
        
        # Parse the output
        # تحليل الخرج
        lines = stdout.splitlines()
        current_profile = None
        for line in lines:
            line = line.strip()
            if "Profile Settings" in line:
                if "Domain Profile" in line:
                    current_profile = "Domain"
                elif "Private Profile" in line:
                    current_profile = "Private"
                elif "Public Profile" in line:
                    current_profile = "Public"
            
            if current_profile and "State" in line:
                if "ON" in line:
                    if current_profile == "Private":
                        is_private_active = True
                    elif current_profile == "Public":
                        is_public_active = True
                    elif current_profile == "Domain":
                        is_domain_active = True
                current_profile = None # Reset for next profile


        # Determine overall status. A firewall is considered active if at least one common profile is ON.
        # تحديد الحالة العامة. يعتبر جدار الحماية نشطًا إذا كان ملف تعريف واحد على الأقل شائعًا في وضع التشغيل.
        if is_private_active or is_public_active or is_domain_active:
            return self._create_result(True, "Windows Defender Firewall is active", "Windows Defender Firewall is enabled on at least one active profile.", "N/A", "Low")
        else:
            return self._create_result(False, "Windows Defender Firewall is inactive", "Windows Defender Firewall is disabled on all active profiles. Your system is exposed.", "Enable Windows Defender Firewall in Control Panel or Settings.", "High")


    def _create_result(self, is_secure, title, description, solution, severity):
        return {
            "check_name": self.check_name,
            "is_secure": is_secure,
            "title": title,
            "description": description,
            "solution": solution,
            "severity": severity
        }
