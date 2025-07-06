# core/checks/antivirus_status.py

from core.utils import run_command, is_linux, is_windows
import datetime

class AntivirusStatusCheck:
    def __init__(self):
        self.check_name = "Antivirus Status"
        self.description = "Verifies if your antivirus software is active and up to date."
        self.solution = "Ensure your antivirus software is enabled, its definitions are updated regularly, and periodic scans are scheduled. If you don't have one, consider installing a reputable antivirus solution."
        self.severity = "High"

    def run_check(self):
        if is_linux():
            return self._check_linux_antivirus()
        elif is_windows():
            return self._check_windows_antivirus()
        else:
            return self._create_result(False, "Unsupported OS", "The current operating system is not supported for this check.", "N/A", "Medium")

    def _check_linux_antivirus(self):
        # We'll primarily check for ClamAV, a common open-source antivirus on Linux.
        
        stdout, stderr, return_code = run_command(["which", "clamscan"])
        if return_code != 0:
            return self._create_result(False, "ClamAV Not Found", "ClamAV (a common Linux antivirus) does not appear to be installed.", "Consider installing ClamAV: 'sudo apt install clamav' or 'sudo pacman -S clamav'", "Medium")

        stdout_daemon, stderr_daemon, return_code_daemon = run_command(["sudo", "systemctl", "is-active", "clamav-daemon"])
        if return_code_daemon == 0 and "active" in stdout_daemon:
            stdout_freshclam, stderr_freshclam, return_code_freshclam = run_command(["sudo", "freshclam", "--stdout", "--verbose"])
            
            if return_code_freshclam == 0 and "ClamAV databases are up to date." in stdout_freshclam:
                return self._create_result(True, "ClamAV Active and Up to Date", "ClamAV daemon is running and its virus definitions are current.", "N/A", "Low")
            else:
                last_update_line = next((line for line in stdout_freshclam.splitlines() if "Last successful update" in line), None)
                if last_update_line:
                    try:
                        date_str = last_update_line.split("Last successful update: ")[1].strip()
                        date_obj = datetime.datetime.strptime(date_str, "%a %b %d %H:%M:%S %Y")
                        
                        time_diff = datetime.datetime.now() - date_obj
                        if time_diff.days > 7: 
                            return self._create_result(False, "ClamAV Definitions Outdated", f"ClamAV daemon is running but definitions were last updated {time_diff.days} days ago.", "Run 'sudo freshclam' to update definitions.", "High")
                        else:
                            return self._create_result(True, "ClamAV Active and Reasonably Up to Date", "ClamAV daemon is running and definitions are recently updated.", "N/A", "Low")
                    except ValueError:
                        return self._create_result(False, "ClamAV Update Status Unknown", "ClamAV daemon is running but could not determine definition update status.", "Manually check ClamAV definition status: 'sudo freshclam -v'", "Medium")
                else:
                    return self._create_result(False, "ClamAV Definitions Not Up to Date", "ClamAV daemon is running but definitions do not appear to be current.", "Run 'sudo freshclam' to update definitions.", "High")
        else:
            return self._create_result(False, "ClamAV Daemon Inactive", "ClamAV is installed but its daemon is not active. Your system might be exposed.", "Start ClamAV daemon: 'sudo systemctl start clamav-daemon && sudo systemctl enable clamav-daemon'", "High")

    def _check_windows_antivirus(self):
        powershell_command = [
            "powershell.exe",
            "-Command",
            "Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntiVirusProduct | Select-Object displayName, productState, pathToSignedProductExe"
        ]
        
        stdout, stderr, return_code = run_command(powershell_command)
        
        if return_code != 0:
            return self._create_result(False, "Antivirus Check Failed", "Could not retrieve antivirus status (possibly due to insufficient permissions or PowerShell execution policy). Please run as administrator.", self.solution, "Medium")

        antivirus_products = []
        current_product_data = {} # استخدم قاموس مؤقت لجمع البيانات لكل منتج

        # قراءة السطور وتجميع البيانات لمنتج واحد
        # Read lines and accumulate data for a single product
        for line in stdout.splitlines():
            line = line.strip()
            if not line: # تخطي السطور الفارغة
                continue
            
            # التحقق من وجود "displayName", "productState", "pathToSignedProductExe" في السطر
            # Check for specific keywords in the line
            if "displayName" in line and ":" in line:
                current_product_data["displayName"] = line.split(":", 1)[1].strip()
            elif "productState" in line and ":" in line:
                try:
                    state_hex = line.split(":", 1)[1].strip()
                    current_product_data["productState"] = int(state_hex, 16)
                except ValueError:
                    current_product_data["productState"] = 0 
            elif "pathToSignedProductExe" in line and ":" in line:
                current_product_data["pathToSignedProductExe"] = line.split(":", 1)[1].strip()

            # عندما نصل إلى سطر جديد لا يحتوي على أي من الكلمات المفتاحية
            # (أو عندما نصل إلى نهاية المخرجات)، قم بإضافة المنتج المكتمل
            # If the line does not contain expected keywords, it might be the end of a product's data block
            # Or if it's the start of another product's data, the current one is complete.
            # A more robust parsing might involve looking for blank lines between product entries.
            # For simplicity now, let's assume if any of the key fields are present, it's part of a product.
            # We'll add the product when all fields are populated or on a blank line.
            
            # هذا جزء يحتاج لتحسين لأنه لا يمكنه التمييز بين المنتجات بشكل صحيح
            # if line.startswith("---") or not line: # Check for separator or blank line (might not be reliable)
            #     if current_product_data:
            #         antivirus_products.append(current_product_data)
            #         current_product_data = {}

        # بعد الانتهاء من جميع السطور، تأكد من إضافة آخر منتج تم تجميعه
        # After processing all lines, ensure the last accumulated product is added
        if current_product_data:
            antivirus_products.append(current_product_data)
        
        # New parsing logic: Parse blocks of output based on known structure
        # منطق تحليل جديد: تحليل كتل المخرجات بناءً على هيكل معروف
        # The output of Select-Object often has blank lines or separators between objects.
        # We will split the output into blocks representing each AntiVirusProduct.
        product_blocks = stdout.strip().split("\r\n\r\n") # يفصل المنتجات بناءً على سطرين فاضيين
        
        antivirus_products_parsed = []
        for block in product_blocks:
            if not block.strip():
                continue
            product_info = {}
            for line in block.splitlines():
                if "displayName" in line and ":" in line:
                    product_info["displayName"] = line.split(":", 1)[1].strip()
                elif "productState" in line and ":" in line:
                    try:
                        state_hex = line.split(":", 1)[1].strip()
                        product_info["productState"] = int(state_hex, 16)
                    except (ValueError, IndexError):
                        product_info["productState"] = 0
                elif "pathToSignedProductExe" in line and ":" in line:
                    product_info["pathToSignedProductExe"] = line.split(":", 1)[1].strip()
            if product_info: # Add if valid product info was parsed from the block
                antivirus_products_parsed.append(product_info)


        active_av_found = False
        outdated_definitions = False
        
        # Use the newly parsed list: antivirus_products_parsed
        for av_product in antivirus_products_parsed: # Iterate over the correctly parsed products
            display_name = av_product.get("displayName", "Unknown AV")
            product_state = av_product.get("productState", 0)

            # ProductState values are bitmasks:
            # Bit 0 (0x0001): Is enabled/active
            # Bit 8 (0x0100): Definitions are up to date
            # Bit 12 (0x1000): Definitions are out of date
            # Bits are usually 0-indexed for state, but the actual value can be large.
            # Example: 0x210000 means enabled (bit 0) and up-to-date (bit 8).
            # We need to check if the relevant bits are set.

            # Check if the AV is enabled (Bit 0 or 0x000000 to 0x001FFF are enabled statuses)
            # A common check for 'enabled' status from ProductState is:
            # The first nibble (4 bits) of the productState value represents the product's status.
            # 0: Disabled, 1: Enabled, 2: Snoozed, 3: Disabled and out of date
            # The second nibble (bits 4-7) represents the virus definition status.
            # 0: Up to date, 1: Out of date, 2: Not available, 3: Not installed
            # The third nibble (bits 8-11) represents the scan engine status.
            # 0: Up to date, 1: Out of date, 2: Not available, 3: Not installed

            # More robust check:
            # The first two hex digits represent security status (enabled, up-to-date, etc.)
            # Common active states are 0x21xxxx or 0x20xxxx
            is_enabled = False
            is_uptodate_definitions = False
            
            # Simplified check based on common states of Windows Defender
            # 0x200000 = Enabled
            # 0x210000 = Enabled and Up-to-date (definitions)
            # 0x214000 = Enabled, Up-to-date (definitions), Real-time protection enabled
            # 0x218000 = Enabled, Up-to-date (definitions), Real-time and firewall enabled
            
            # Check if the product state indicates it's enabled (usually bit 0 is set for enabled)
            # and potentially if definitions are up to date (bit 8 set)
            if product_state & 0x100000: # If bit 12 (out of date) is NOT set, and bit 8 is set
                is_uptodate_definitions = True
            
            # A product is considered enabled if the first nibble is 0x0 or 0x1 (meaning enabled/not enabled)
            # or if the entire state is one of the "active" states (e.g., 0x210000)
            if (product_state & 0x000001) or (product_state & 0x200000): # Basic check for active bit or common active state
                 is_enabled = True

            # Refined check for up-to-date definitions:
            # The lower byte usually indicates the "status" of components
            # Bit 0: product enabled
            # Bit 1: definitions up to date
            # Bit 2: real-time protection enabled
            # ... this can vary by AV.
            # For simplicity, we'll look for specific state patterns or a combination of bits
            # A common state for "enabled and up-to-date" is where the last two nibbles are 0x10, 0x11, 0x14, 0x15, etc.
            # Or directly check the full productState value.
            
            # Windows Defender: 0x210000 usually means fully enabled and up-to-date
            # Bit 8 (0x0100) indicates definitions are up to date
            # Bit 12 (0x1000) indicates definitions are out of date (we want this to be 0)
            
            # So, if (product_state & 0x100000) is 0 (not out of date)
            # AND (product_state & 0x010000) is 1 (up to date)
            # AND (product_state & 0x000001) is 1 (enabled)
            
            # More simple: if productState indicates it's healthy.
            # Healthy states usually start with 0x2 or 0x3 (e.g., 0x210000, 0x310000)
            # Let's consider any product state that implies "enabled" AND "definitions are not out of date"
            
            # Check if enabled: (Bit 0 = 1 for enabled)
            is_enabled = bool(product_state & 0x1000) # This is a common bit for active status (different from 0x0001)
            # Check if definitions are up-to-date (Bit 8 = 1) and not out of date (Bit 12 = 0)
            definitions_current = bool(product_state & 0x0100) and not bool(product_state & 0x1000) # This needs re-evaluation

            # Re-checking ProductState logic based on common interpretations:
            # The last 6 digits of productState (first three hex bytes) describe the product status
            # Example: 0x210000
            # Byte 1 (first hex pair): Product status (00 = disabled, 10 = enabled, 20 = enabled & running)
            # Byte 2 (second hex pair): Virus definition status (00 = up to date, 10 = out of date)
            # Byte 3 (third hex pair): Engine status (00 = up to date, 10 = out of date)
            
            # This is simpler:
            is_enabled = (product_state & 0xF00000) in [0x100000, 0x200000, 0x300000] # Check first hex digit (nibble) for enabled
            # Is definitions up to date? Check the relevant bit / nibble.
            definitions_up_to_date = bool(product_state & 0x000010) # Often bit 4 indicates if AV is fully up to date

            # Let's simplify and use common well-known states for Windows Defender.
            # 0x210000 = Windows Defender is On and Up To Date
            # 0x200000 = Windows Defender is On (but may not be up to date)
            # 0x000000 = Windows Defender is Off
            
            if product_state >= 0x200000: # Implies enabled and potentially up to date
                active_av_found = True
                if product_state < 0x210000: # If it's enabled but not specifically 0x21xxxx, it might be outdated
                    outdated_definitions = True
                    break # Found an active AV with potentially outdated definitions
            elif product_state >= 0x100000: # Enabled but not fully running/up to date
                active_av_found = True
                outdated_definitions = True
                break

        if not active_av_found:
            return self._create_result(False, "No Active Antivirus Found", "No active antivirus product was detected on your system.", self.solution, "High")
        elif outdated_definitions:
            return self._create_result(False, "Antivirus Definitions Outdated", "An active antivirus was found, but its definitions are outdated or status is not fully healthy.", self.solution, "High")
        else:
            return self._create_result(True, "Antivirus Active and Up to Date", "Your antivirus software is active and its definitions appear to be up to date.", "N/A", "Low")


    def _create_result(self, is_secure, title, description, solution, severity):
        return {
            "check_name": self.check_name,
            "is_secure": is_secure,
            "title": title,
            "description": description,
            "solution": solution,
            "severity": severity
        }
