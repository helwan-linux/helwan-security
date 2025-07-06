# core/checks/open_ports.py
# Checks for open network ports that could be security vulnerabilities.

from core.utils import run_command, is_linux, is_windows

class OpenPortsCheck:
    def __init__(self):
        self.check_name = "Open Network Ports"
        self.description = "Identifies open network ports on your system that might expose services to unauthorized access."
        self.solution = "Close unnecessary open ports. Configure your firewall to block incoming connections to unused ports. Ensure only essential services are running and accessible."
        self.severity = "High"

    def run_check(self):
        if is_linux():
            return self._check_linux_open_ports()
        elif is_windows():
            return self._check_windows_open_ports()
        else:
            return self._create_result(False, "Unsupported OS", "The current operating system is not supported for this check.", "N/A", "Medium")

    def _check_linux_open_ports(self):
        # Use 'ss -tuln' or 'netstat -tuln' to list listening TCP/UDP ports
        # استخدام 'ss -tuln' أو 'netstat -tuln' لسرد منافذ TCP/UDP المستمعة
        command = ["ss", "-tuln"]
        stdout, stderr, return_code = run_command(command)

        if return_code != 0:
            # إذا فشل الأمر، جرب netstat كبديل (خاصة في الأنظمة القديمة)
            command = ["netstat", "-tuln"]
            stdout, stderr, return_code = run_command(command)
            if return_code != 0:
                return self._create_result(False, "Failed to check open ports", f"Could not run 'ss' or 'netstat' command: {stderr}", self.solution, "Medium")

        open_ports = []
        for line in stdout.splitlines():
            # Lines like: tcp   LISTEN 0      128    127.0.0.1:631        0.0.0.0:*
            # أو: tcp        0      0 0.0.0.0:22              0.0.0.0:* LISTEN     
            if "LISTEN" in line:
                # محاولة استخراج عنوان IP والمنفذ
                parts = line.split()
                # البحث عن الجزء الذي يحتوي على IP:Port
                for part in parts:
                    if ":" in part and "." in part and part.count(':') == 1: # Basic check for IP:Port
                        # مثال: 0.0.0.0:22 أو 127.0.0.1:631
                        if "*" in part: # إذا كان المنفذ يستمع على جميع الواجهات
                            open_ports.append(f"*{part.split(':')[1]}") 
                        else:
                            open_ports.append(part)
                        break # لقينا المنفذ، ننتقل للسطر التالي

        # إزالة التكرارات
        open_ports = sorted(list(set(open_ports)))

        if open_ports:
            # تم العثور على منافذ مفتوحة
            description = f"The following ports are open and listening: {', '.join(open_ports)}. Review them to ensure they are necessary."
            return self._create_result(False, "Open Ports Detected", description, self.solution, "High")
        else:
            # لا توجد منافذ مفتوحة (من خلال الفحص)
            return self._create_result(True, "No Open Ports Detected", "No unauthorized open ports were found listening on your system.", "N/A", "Low")

    def _check_windows_open_ports(self):
        # Use 'netstat -an' to list all active connections and listening ports
        # استخدام 'netstat -an' لسرد جميع الاتصالات النشطة والمنافذ المستمعة
        command = ["netstat", "-an"]
        stdout, stderr, return_code = run_command(command)

        if return_code != 0:
            return self._create_result(False, "Failed to check open ports", f"Could not run 'netstat' command: {stderr}", self.solution, "Medium")

        open_ports = []
        for line in stdout.splitlines():
            # Lines look like:   TCP    0.0.0.0:135            0.0.0.0:0              LISTENING
            if "LISTENING" in line:
                parts = line.strip().split()
                if len(parts) >= 2:
                    # المنفذ المحلي هو الجزء الثاني
                    local_address_port = parts[1] 
                    if local_address_port and ":" in local_address_port:
                        # استخراج المنفذ فقط
                        port = local_address_port.split(':')[-1]
                        open_ports.append(f"{port} ({parts[0]})") # نضف نوع البروتوكول (TCP/UDP)

        # إزالة التكرارات
        open_ports = sorted(list(set(open_ports)))

        # تجاهل المنافذ المعروفة والآمنة نسبياً (مثلاً، المنافذ العابرة التي تستخدمها تطبيقات عادية)
        # هذا الترشيح يمكن تعديله بناءً على ما تريد تجاهله
        # Ports that are commonly open for legitimate reasons and are often not a direct security risk unless misused.
        # This list is highly dependent on typical usage and should be refined.
        # أمثلة للمنافذ الشائعة التي قد لا تشكل خطراً مباشراً إذا كانت ضرورية لتشغيل النظام أو التطبيقات العادية
        ignored_ports = [
            "135 (TCP)", # RPC
            "445 (TCP)", # SMB
            "5357 (TCP)", # WS-Discovery
            "5357 (UDP)",
            "1900 (UDP)", # SSDP
            "500 (UDP)", # IKEv2 for VPN
            # أضف هنا أي منافذ أخرى تعرف أنها تفتحها تطبيقاتك الشرعية بشكل متكرر
        ]
        
        filtered_open_ports = [p for p in open_ports if p not in ignored_ports]


        if filtered_open_ports:
            # تم العثور على منافذ مفتوحة غير معروفة
            description = f"The following non-standard/potentially unnecessary ports are open and listening: {', '.join(filtered_open_ports)}. Review them to ensure they are essential."
            return self._create_result(False, "Open Ports Detected", description, self.solution, "High")
        else:
            # لا توجد منافذ مفتوحة (من خلال الفحص) أو كلها منافذ آمنة
            return self._create_result(True, "No Critical Open Ports Detected", "No potentially unauthorized or critical open ports were found listening on your system.", "N/A", "Low")


    def _create_result(self, is_secure, title, description, solution, severity):
        return {
            "check_name": self.check_name,
            "is_secure": is_secure,
            "title": title,
            "description": description,
            "solution": solution,
            "severity": severity
        }
