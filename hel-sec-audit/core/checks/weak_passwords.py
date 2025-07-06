# core/checks/weak_passwords.py

from core.utils import run_command, is_linux, is_windows

class WeakPasswordsCheck:
    def __init__(self):
        self.check_name = "Weak Password Policies/Usage"
        self.description = "Checks for weak password policies and common vulnerabilities related to user passwords."
        self.solution = "Implement strong password policies (e.g., minimum length, complexity, regular changes). Educate users about choosing strong, unique passwords and consider using a password manager. Ensure no empty passwords are used."
        self.severity = "High"

    def run_check(self):
        if is_linux():
            return self._check_linux_passwords()
        elif is_windows():
            return self._check_windows_passwords()
        else:
            return self._create_result(False, "Unsupported OS", "The current operating system is not supported for this check.", "N/A", "Medium")

    def _check_linux_passwords(self):
        # Check for empty passwords in /etc/shadow
        # فحص وجود كلمات مرور فارغة في ملف /etc/shadow
        stdout, stderr, return_code = run_command(["sudo", "awk", "-F:", '($2 == "") {print}', "/etc/shadow"], sudo_required=True)
        if return_code == 0 and stdout.strip():
            empty_password_users = stdout.strip().splitlines()
            description = f"Users with empty passwords found: {', '.join([user.split(':')[0] for user in empty_password_users])}. This is a critical security vulnerability."
            return self._create_result(False, "Empty Passwords Found", description, "Set strong passwords for these users immediately. Run 'sudo passwd <username>' for each.", "Critical")
        
        # Check for system-wide password policy using /etc/login.defs
        # فحص سياسة كلمة المرور على مستوى النظام باستخدام /etc/login.defs
        min_len_found = False
        min_len_val = 0
        try:
            with open("/etc/login.defs", "r") as f:
                for line in f:
                    if line.strip().startswith("PASS_MIN_LEN"):
                        parts = line.strip().split()
                        if len(parts) > 1 and parts[1].isdigit():
                            min_len_val = int(parts[1])
                            min_len_found = True
                            break
        except FileNotFoundError:
            # If login.defs is not found, cannot determine policy easily
            pass
        except Exception as e:
            print(f"Error reading /etc/login.defs: {e}") # لغرض التصحيح المؤقت، يمكن إزالته لاحقًا

        if min_len_found and min_len_val < 8: # Recommended minimum length is 8 characters or more
            description = f"Password minimum length (PASS_MIN_LEN) is set to {min_len_val} in /etc/login.defs, which is too short. Recommended 8 or more characters."
            return self._create_result(False, "Weak Password Minimum Length Policy", description, "Edit /etc/login.defs and set PASS_MIN_LEN to at least 8.", "High")
        
        # Check for password complexity requirements (more advanced, often done by pam)
        # هذا فحص مبدئي وقد يتطلب فحص PAM بشكل أعمق للمزيد من الدقة
        stdout_pam, stderr_pam, return_code_pam = run_command(["grep", "-r", "pam_pwquality.so", "/etc/pam.d/"])
        if return_code_pam != 0 or not stdout_pam:
             description = "No clear indication of a strong password quality module (like pam_pwquality.so) being enforced."
             return self._create_result(False, "Potential Lack of Password Complexity Policy", description, "Ensure PAM modules like 'pam_pwquality.so' are configured to enforce complexity requirements (e.g., mixtlf, dcredit, ucredit, ocredit).", "Medium")

        return self._create_result(True, "Linux Password Policies Appear Adequate", "No critical weak password policy issues or empty passwords detected.", "N/A", "Low")

    def _check_windows_passwords(self):
        # Check Windows Password Policy using 'net accounts'
        # فحص سياسة كلمة المرور في ويندوز باستخدام 'net accounts'
        stdout, stderr, return_code = run_command(["net", "accounts"])

        if return_code != 0:
            return self._create_result(False, "Windows Password Policy Check Failed", "Could not retrieve password policy (possibly due to insufficient permissions). Please run as administrator.", self.solution, "Medium")

        policy_details = {}
        for line in stdout.splitlines():
            line = line.strip()
            if "minimum password length" in line:
                policy_details["min_len"] = int(line.split()[-2])
            elif "password history length" in line:
                policy_details["history_len"] = int(line.split()[-2])
            elif "maximum password age (days)" in line:
                val = line.split()[-2]
                policy_details["max_age"] = int(val) if val.isdigit() else 0 # 0 for Never Expires
            elif "minimum password age (days)" in line:
                val = line.split()[-2]
                policy_details["min_age"] = int(val) if val.isdigit() else 0
            elif "password must meet complexity requirements" in line:
                policy_details["complexity"] = "Yes" in line

        issues = []
        if policy_details.get("min_len", 0) < 8:
            issues.append(f"Minimum password length is {policy_details.get('min_len', 0)}, recommended is 8 or more.")
        if not policy_details.get("complexity", False):
            issues.append("Password complexity requirements are not enabled.")
        if policy_details.get("history_len", 0) < 5: # Recommended history is at least 5
            issues.append(f"Password history length is {policy_details.get('history_len', 0)}, recommended is 5 or more.")
        if policy_details.get("max_age", 0) == 0: # If max_age is 0, passwords never expire
            issues.append("Passwords are set to never expire (Maximum Password Age is 0).")

        if issues:
            description = "Your Windows password policy has weaknesses:\n" + "\n".join(issues)
            return self._create_result(False, "Weak Windows Password Policy", description, self.solution, "High")
        else:
            return self._create_result(True, "Windows Password Policies Appear Adequate", "Your Windows password policies meet recommended security standards.", "N/A", "Low")


    def _create_result(self, is_secure, title, description, solution, severity):
        return {
            "check_name": self.check_name,
            "is_secure": is_secure,
            "title": title,
            "description": description,
            "solution": solution,
            "severity": severity
        }
