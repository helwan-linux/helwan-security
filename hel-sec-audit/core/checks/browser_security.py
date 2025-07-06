# core/checks/browser_security.py
# Checks security settings of common web browsers.

from core.utils import is_windows, is_linux, run_command
import os
import json
import sqlite3 # Firefox uses SQLite databases for some settings

class BrowserSecurityCheck:
    def __init__(self):
        self.check_name = "Browser Security Settings"
        self.description = "Examines key security configurations of common web browsers (Chrome, Firefox) to identify potential vulnerabilities."
        self.solution = "Enable HTTPS-Only Mode, Enhanced Tracking Protection, Secure DNS, and ensure Phishing/Malware protection is active in your browser settings. Keep your browser updated."
        self.severity = "High"

    def run_check(self):
        results = []

        if is_windows():
            results.append(self._check_chrome_windows())
            results.append(self._check_firefox_windows())
        elif is_linux():
            results.append(self._check_chrome_linux())
            results.append(self._check_firefox_linux())
        else:
            results.append(self._create_result(False, "Unsupported OS for Browser Check", "Browser security checks are not supported on this operating system.", "N/A", "Medium"))
        
        # Combine individual browser results into a single overall result
        # دمج نتائج المتصفحات الفردية في نتيجة إجمالية
        overall_is_secure = all(r["is_secure"] for r in results if r is not None)
        overall_title = "All Supported Browsers Appear Secure" if overall_is_secure else "Potential Browser Security Weaknesses Detected"
        overall_description = "Reviewed security settings for supported browsers. See individual browser results for details."
        overall_solution = self.solution
        overall_severity = "Low" if overall_is_secure else "High"

        # You might want to return a list of individual results, or one combined result with details.
        # For simplicity, let's return one combined result and list issues from all.
        
        combined_issues = []
        for r in results:
            if r and not r["is_secure"]:
                combined_issues.append(f"{r['check_name']} ({r['title']}): {r['description']}")
        
        if combined_issues:
            overall_description = "The following browser security issues were found:\n" + "\n".join(combined_issues)
            return self._create_result(overall_is_secure, overall_title, overall_description, overall_solution, overall_severity)
        else:
            return self._create_result(overall_is_secure, overall_title, overall_description, overall_solution, overall_severity)


    def _check_chrome_windows(self):
        # Chrome settings are stored in preferences file as JSON
        # Path: %LOCALAPPDATA%\Google\Chrome\User Data\Default\Preferences
        # Or in the Registry (less common for specific settings)
        chrome_path = os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\User Data")
        default_profile_path = os.path.join(chrome_path, "Default", "Preferences")

        if not os.path.exists(default_profile_path):
            return self._create_result(True, "Chrome Not Found/Config Unavailable (Windows)", "Google Chrome browser configuration file not found. Please ensure Chrome is installed and used.", "N/A", "Low") # Not vulnerable, just not found

        try:
            with open(default_profile_path, "r", encoding="utf-8") as f:
                prefs = json.load(f)
            
            issues = []

            # Check Safe Browse (Phishing/Malware protection)
            safe_Browse_enabled = prefs.get("safeBrowse", {}).get("enabled", False)
            if not safe_Browse_enabled:
                issues.append("Safe Browse (Phishing/Malware protection) is disabled.")
            
            # Check for Secure DNS (DNS-over-HTTPS)
            # This setting is not directly in Preferences, but often managed via command line flags or group policy
            # It's hard to programmatically verify without deep parsing or admin tools.
            # For simplicity, we might skip this for now or check a less direct indicator.
            # Let's skip secure DNS check for Chrome for now due to complexity.

            # Check Third-party cookies status
            # prefs.content_settings.exceptions.cookies (can be complex)
            # A simpler approach is to check default behavior:
            cookie_default = prefs.get("profile", {}).get("default_content_settings", {}).get("cookies", 0)
            # 0: Allow all, 1: Block third-party (Chrome default), 2: Block all
            if cookie_default == 0:
                issues.append("Third-party cookies are allowed (potential for tracking).")
            
            if issues:
                description = "Chrome security issues: \n" + "\n".join(issues)
                return self._create_result(False, "Weak Chrome Security Settings (Windows)", description, self.solution, self.severity)
            else:
                return self._create_result(True, "Chrome Security Settings Appear Good (Windows)", "Key Chrome security settings are enabled.", "N/A", "Low")

        except Exception as e:
            return self._create_result(False, "Chrome Config Read Error (Windows)", f"Could not read Chrome preferences: {e}", "Ensure Chrome is closed and try again, or check file permissions.", "Medium")


    def _check_firefox_windows(self):
        # Firefox settings are in prefs.js within the profile folder
        # Path: %APPDATA%\Mozilla\Firefox\Profiles\<profile_id>\prefs.js
        # Or some advanced settings in about:config which are stored in 'user.js'
        # Some settings are also in places.sqlite for site permissions.

        firefox_path = os.path.expandvars(r"%APPDATA%\Mozilla\Firefox\Profiles")
        
        if not os.path.exists(firefox_path):
            return self._create_result(True, "Firefox Not Found (Windows)", "Mozilla Firefox browser profile folder not found. Please ensure Firefox is installed and used.", "N/A", "False Negative")
        
        profile_dirs = [d for d in os.listdir(firefox_path) if os.path.isdir(os.path.join(firefox_path, d)) and ".default" in d]
        
        if not profile_dirs:
            return self._create_result(True, "Firefox Profile Not Found (Windows)", "No Firefox default profile found.", "N/A", "False Negative")

        profile_path = os.path.join(firefox_path, profile_dirs[0]) # Take the first default profile
        prefs_js_path = os.path.join(profile_path, "prefs.js")

        if not os.path.exists(prefs_js_path):
            return self._create_result(True, "Firefox Config Unavailable (Windows)", "Firefox prefs.js file not found. Please ensure Firefox is installed and used.", "N/A", "False Negative")

        try:
            issues = []
            prefs_content = ""
            with open(prefs_js_path, "r", encoding="utf-8", errors="ignore") as f:
                prefs_content = f.read()

            # Check HTTPS-Only Mode (network.http.security.enable_https_only_mode)
            if 'user_pref("network.http.security.enable_https_only_mode", false);' in prefs_content:
                issues.append("HTTPS-Only Mode is disabled.")

            # Check Enhanced Tracking Protection (privacy.trackingprotection.enabled)
            if 'user_pref("privacy.trackingprotection.enabled", false);' in prefs_content:
                issues.append("Enhanced Tracking Protection is disabled.")
            
            # Check Secure DNS (network.trr.mode)
            # 0=off, 1=opportunistic, 2=secure only, 3=secure only for certain domains
            # We want mode 2 or 3 for strong security
            if 'user_pref("network.trr.mode", 0);' in prefs_content or \
               'user_pref("network.trr.mode", 1);' in prefs_content:
                issues.append("Secure DNS (DNS-over-HTTPS/TLS) is not configured for 'secure only' mode.")

            # Check Phishing and Malware Protection (browser.safeBrowse.enabled)
            if 'user_pref("browser.safeBrowse.enabled", false);' in prefs_content or \
               'user_pref("browser.safeBrowse.malware.enabled", false);' in prefs_content or \
               'user_pref("browser.safeBrowse.phishing.enabled", false);' in prefs_content:
                issues.append("Phishing and/or Malware Protection is disabled.")
            
            if issues:
                description = "Firefox security issues: \n" + "\n".join(issues)
                return self._create_result(False, "Weak Firefox Security Settings (Windows)", description, self.solution, self.severity)
            else:
                return self._create_result(True, "Firefox Security Settings Appear Good (Windows)", "Key Firefox security settings are enabled.", "N/A", "Low")

        except Exception as e:
            return self._create_result(False, "Firefox Config Read Error (Windows)", f"Could not read Firefox preferences: {e}", "Ensure Firefox is closed and try again, or check file permissions.", "Medium")

    def _check_chrome_linux(self):
        # Chrome settings on Linux are similar to Windows, stored in Preferences JSON.
        # Path: ~/.config/google-chrome/Default/Preferences
        chrome_path = os.path.expanduser("~/.config/google-chrome")
        default_profile_path = os.path.join(chrome_path, "Default", "Preferences")

        if not os.path.exists(default_profile_path):
            return self._create_result(True, "Chrome Not Found/Config Unavailable (Linux)", "Google Chrome browser configuration file not found. Please ensure Chrome is installed and used.", "N/A", "Low")

        try:
            with open(default_profile_path, "r", encoding="utf-8") as f:
                prefs = json.load(f)
            
            issues = []

            safe_Browse_enabled = prefs.get("safeBrowse", {}).get("enabled", False)
            if not safe_Browse_enabled:
                issues.append("Safe Browse (Phishing/Malware protection) is disabled.")
            
            cookie_default = prefs.get("profile", {}).get("default_content_settings", {}).get("cookies", 0)
            if cookie_default == 0:
                issues.append("Third-party cookies are allowed (potential for tracking).")
            
            if issues:
                description = "Chrome security issues: \n" + "\n".join(issues)
                return self._create_result(False, "Weak Chrome Security Settings (Linux)", description, self.solution, self.severity)
            else:
                return self._create_result(True, "Chrome Security Settings Appear Good (Linux)", "Key Chrome security settings are enabled.", "N/A", "Low")

        except Exception as e:
            return self._create_result(False, "Chrome Config Read Error (Linux)", f"Could not read Chrome preferences: {e}", "Ensure Chrome is closed and try again, or check file permissions.", "Medium")

    def _check_firefox_linux(self):
        # Firefox settings on Linux are similar to Windows, in prefs.js
        # Path: ~/.mozilla/firefox/<profile_id>/prefs.js
        firefox_path = os.path.expanduser("~/.mozilla/firefox")
        
        if not os.path.exists(firefox_path):
            return self._create_result(True, "Firefox Not Found (Linux)", "Mozilla Firefox browser profile folder not found. Please ensure Firefox is installed and used.", "N/A", "False Negative")
        
        profile_dirs = [d for d in os.listdir(firefox_path) if os.path.isdir(os.path.join(firefox_path, d)) and ".default" in d]
        
        if not profile_dirs:
            return self._create_result(True, "Firefox Profile Not Found (Linux)", "No Firefox default profile found.", "N/A", "False Negative")

        profile_path = os.path.join(firefox_path, profile_dirs[0])
        prefs_js_path = os.path.join(profile_path, "prefs.js")

        if not os.path.exists(prefs_js_path):
            return self._create_result(True, "Firefox Config Unavailable (Linux)", "Firefox prefs.js file not found. Please ensure Firefox is installed and used.", "N/A", "False Negative")

        try:
            issues = []
            prefs_content = ""
            with open(prefs_js_path, "r", encoding="utf-8", errors="ignore") as f:
                prefs_content = f.read()

            if 'user_pref("network.http.security.enable_https_only_mode", false);' in prefs_content:
                issues.append("HTTPS-Only Mode is disabled.")

            if 'user_pref("privacy.trackingprotection.enabled", false);' in prefs_content:
                issues.append("Enhanced Tracking Protection is disabled.")
            
            if 'user_pref("network.trr.mode", 0);' in prefs_content or \
               'user_pref("network.trr.mode", 1);' in prefs_content:
                issues.append("Secure DNS (DNS-over-HTTPS/TLS) is not configured for 'secure only' mode.")

            if 'user_pref("browser.safeBrowse.enabled", false);' in prefs_content or \
               'user_pref("browser.safeBrowse.malware.enabled", false);' in prefs_content or \
               'user_pref("browser.safeBrowse.phishing.enabled", false);' in prefs_content:
                issues.append("Phishing and/or Malware Protection is disabled.")
            
            if issues:
                description = "Firefox security issues: \n" + "\n".join(issues)
                return self._create_result(False, "Weak Firefox Security Settings (Linux)", description, self.solution, self.severity)
            else:
                return self._create_result(True, "Firefox Security Settings Appear Good (Linux)", "Key Firefox security settings are enabled.", "N/A", "Low")

        except Exception as e:
            return self._create_result(False, "Firefox Config Read Error (Linux)", f"Could not read Firefox preferences: {e}", "Ensure Firefox is closed and try again, or check file permissions.", "Medium")


    def _create_result(self, is_secure, title, description, solution, severity):
        return {
            "check_name": self.check_name,
            "is_secure": is_secure,
            "title": title,
            "description": description,
            "solution": solution,
            "severity": severity
        }
