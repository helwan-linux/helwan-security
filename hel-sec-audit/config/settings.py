# config/settings.py
# Contains application settings and configurations.

# Default settings for scan preferences
# الإعدادات الافتراضية لتفضيلات الفحص
DEFAULT_SCAN_PREFERENCES = {
    "scan_system_updates": True,
    "scan_weak_passwords": True,
    "scan_open_ports": True,
    "scan_firewall_status": True,
    # أضف المزيد من تفضيلات الفحص هنا
}

# Default report output path
# المسار الافتراضي لإخراج التقرير
DEFAULT_REPORT_PATH = "data/reports/"

# You can add functions to load/save settings from/to a file (e.g., JSON)
# يمكنك إضافة دوال لتحميل/حفظ الإعدادات من/إلى ملف (على سبيل المثال، JSON)