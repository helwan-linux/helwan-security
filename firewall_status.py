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
        
        # 1. الفحص الأكثر عمومية: فحص وجود قواعد تصفية مُحملة في نواة النظام (Netfilter/IPtables)
        # هذا يغطي أي جدار حماية (UFW, Firewalld, nftables, Custom Scripts, إلخ) يعمل على Linux.
        command_iptables = ["sudo", "iptables", "-L", "INPUT"]
        stdout_iptables, stderr_iptables, return_code_iptables = run_command(command_iptables)

        if return_code_iptables == 0:
            # 1.1 التحقق من السياسة الافتراضية (Policy)
            # إذا كانت السياسة الافتراضية DROP/REJECT، فهذا يعني حماية أساسية (مُفعّل)
            if "policy ACCEPT" not in stdout_iptables.splitlines()[0].upper():
                return self._create_result(True, "Firewall is Active (Restrictive Policy)", "The default packet filtering policy is restrictive (DROP/REJECT).", "N/A", "Low")
            
            # 1.2 التحقق من وجود قواعد فعلية (أكثر من سطرين هيدر)
            # إذا كان هناك أكثر من سطرين (وهما سطر العنوان وسطر السياسة)، فهذا يعني وجود قواعد تصفية مُحملة.
            if len(stdout_iptables.splitlines()) > 2:
                # القواعد مُحملة، بغض النظر عن السياسة الافتراضية
                return self._create_result(True, "Firewall is Active (Filtering Rules Loaded)", "Specific filtering rules are loaded in the Linux kernel (IPtables/NFTables).", "N/A", "Low")
        
        # 2. الفحص الاحتياطي: التحقق من حالة خدمات جدار الحماية الشائعة
        # يتم اللجوء إلى هذا الفحص في حال عدم قدرة البرنامج على قراءة iptables (فشل sudo) أو في حال كانت الجداول فارغة.

        # 2.1 التحقق من UFW باستخدام systemctl (لتجاوز مشاكل sudo في البيئة الرسومية)
        stdout_ufw_active, _, return_code_active = run_command(["systemctl", "is-active", "ufw"])
        if return_code_active == 0 and "active" in stdout_ufw_active:
            # UFW يعمل كخدمة ومُفعّل
            return self._create_result(True, "Firewall is Active (UFW Service Running)", "UFW service is running and configured.", "N/A", "Low")
        
        # 2.2 التحقق من Firewalld
        stdout_fw_active, _, return_code_fw_active = run_command(["systemctl", "is-active", "firewalld"])
        if return_code_fw_active == 0 and "active" in stdout_fw_active:
            # Firewalld يعمل كخدمة ومُفعّل
            return self._create_result(True, "Firewall is Active (Firewalld Service Running)", "Firewalld service is running and configured.", "N/A", "Low")
            
        # 3. النتيجة النهائية (Firewall is Inactive/Unknown)
        # في هذه الحالة، لم نجد أي دليل على وجود حماية فعّالة.
        
        # إذا فشل أمر iptables بسبب الأذونات
        if return_code_iptables != 0 and "permission denied" in stderr_iptables.lower():
            # هذه هي الحالة التي تسببت في الخطأ الثابت الذي رأيته سابقاً
             return self._create_result(
                 False, 
                 "Firewall Status Unknown (Permissions Issue)", 
                 "Could not verify firewall status due to insufficient privileges. The firewall might be active but cannot be confirmed.", 
                 "Run the application with administrator (sudo) privileges to confirm firewall status.", 
                 "Medium"
             )

        # الحالة الافتراضية: لا يوجد حماية
        return self._create_result(
            False, 
            "Firewall is Inactive or Unconfigured", 
            "No active packet filtering rules or common firewall services were detected. Your system is exposed.", 
            "Install and enable a firewall (e.g., 'sudo ufw enable' or configure Netfilter rules).", 
            "High"
        )


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
