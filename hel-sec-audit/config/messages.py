# config/messages.py
# Centralized location for all user-facing messages and solution texts.
# هذا ملف مركزي لجميع الرسائل الموجهة للمستخدم ونصوص الحلول.

# General messages
APP_TITLE = "hel-sec-audit"
START_SCAN_BUTTON_TEXT = "Start Scan"
SETTINGS_BUTTON_TEXT = "Settings"
ABOUT_BUTTON_TEXT = "About"
GENERATE_REPORT_BUTTON_TEXT = "Generate PDF Report"
CLOSE_BUTTON_TEXT = "Close"
BROWSE_BUTTON_TEXT = "Browse..."
SAVE_SETTINGS_BUTTON_TEXT = "Save Settings"

# Scan status messages
SCAN_INITIALIZING_MESSAGE = "Initializing scan..."
SCAN_RUNNING_MESSAGE = "Running check: {}..." # Placeholder for check name
SCAN_COMPLETE_MESSAGE = "Scan Complete!"

# Check-specific messages (examples)
# رسائل خاصة بكل فحص (أمثلة)
SYSTEM_UPDATES_SOLUTION = "Run system update commands (e.g., 'sudo pacman -Syu' on Arch Linux, 'sudo apt update && sudo apt upgrade' on Debian/Ubuntu, or use 'Windows Update' on Windows)."
WEAK_PASSWORDS_SOLUTION = "Ensure strong password policies are enforced. Avoid common or easily guessable passwords. Change any identified weak passwords immediately."
OPEN_PORTS_SOLUTION = "Close unnecessary open ports using your system's firewall (e.g., UFW on Linux, Windows Defender Firewall). Ensure only essential services are exposed."
FIREWALL_STATUS_SOLUTION = "Enable your system's firewall (e.g., UFW on Linux, Windows Defender Firewall) and ensure it's configured to block unnecessary incoming connections."

# Report messages
REPORT_SUMMARY_TITLE = "Scan Summary"
REPORT_DETAILS_TITLE = "Detailed Findings"
REPORT_TOTAL_CHECKS = "Total checks performed: {}"
REPORT_ISSUES_FOUND = "Issues found: {}"
REPORT_CHECK_NAME = "Check:"
REPORT_STATUS = "Status:"
REPORT_SEVERITY = "Severity:"
REPORT_DESCRIPTION = "Description:"
REPORT_SOLUTION = "Solution:"
REPORT_SECURE_STATUS = "Secure"
REPORT_VULNERABLE_STATUS = "Vulnerable"

# About window messages
ABOUT_VERSION = "Version: 0.1.0"
ABOUT_DEVELOPER = "Developed by: [Your Name/Team Name]"
ABOUT_COPYRIGHT = "© 2025 All rights reserved."
ABOUT_DESCRIPTION = "This tool is designed to enhance the security posture of your system."

# Error messages
ERROR_LOGO_NOT_FOUND = "Error: logo.png not found or could not be loaded."
ERROR_UNSUPPORTED_OS = "The current operating system is not supported for this check."
ERROR_COMMAND_NOT_FOUND = "Error: Command '{}' not found."
ERROR_UNEXPECTED = "An unexpected error occurred: {}"