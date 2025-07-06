# core/config_manager.py
# Manages application configuration settings.

import json
import os

class ConfigManager:
    def __init__(self, config_file="config.json"):
        # تحديد مسار ملف الإعدادات
        # يتم وضع ملف الإعدادات بجانب ملف main.py أو في مجلد فرعي للبيانات
        # لغرض البساطة والتطوير الحالي، سنضعه في نفس مسار تشغيل التطبيق
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.config_path = os.path.join(script_dir, config_file)
        # إذا كنت تفضل وضعه في مجلد البيانات بدلاً من core
        # self.config_path = os.path.join(os.path.dirname(script_dir), config_file) 
        
        self.default_config = {
            "checks_enabled": {
                "System Updates Status": True,
                "Weak Password Policies/Usage": True,
                "Open Network Ports": True,
                "Firewall Status": True
            },
            "general_settings": {
                "dark_mode": False # مثال لإعداد عام آخر
            }
        }
        self.config = self._load_config()

    def _load_config(self):
        # تحميل الإعدادات من الملف، أو استخدام الإعدادات الافتراضية إذا لم يكن موجوداً
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, "r") as f:
                    loaded_config = json.load(f)
                    # دمج الإعدادات المحملة مع الافتراضية لضمان وجود جميع المفاتيح
                    # هذا يضمن أن الإعدادات الجديدة تضاف تلقائياً إذا قمنا بتوسيع default_config
                    merged_config = self.default_config.copy()
                    for key, value in loaded_config.items():
                        if isinstance(value, dict) and key in merged_config:
                            merged_config[key].update(value)
                        else:
                            merged_config[key] = value
                    return merged_config
            except json.JSONDecodeError:
                # في حالة تلف ملف الإعدادات، يتم استخدام الإعدادات الافتراضية
                print(f"Warning: Corrupted config file '{self.config_path}'. Using default settings.")
                return self.default_config
        # إذا لم يكن الملف موجوداً
        return self.default_config

    def save_config(self):
        # حفظ الإعدادات الحالية في الملف
        try:
            with open(self.config_path, "w") as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Error saving config file: {e}")

    def get_setting(self, category, key):
        # الحصول على قيمة إعداد معين
        return self.config.get(category, {}).get(key)

    def set_setting(self, category, key, value):
        # تعيين قيمة لإعداد معين
        if category not in self.config:
            self.config[category] = {}
        self.config[category][key] = value
        self.save_config() # حفظ التغيير فوراً

    def get_all_check_settings(self):
        # الحصول على حالة تمكين/تعطيل جميع الفحوصات
        return self.config.get("checks_enabled", {})
    
    def set_check_enabled(self, check_name, enabled):
        # تعيين حالة تمكين/تعطيل فحص معين
        if "checks_enabled" not in self.config:
            self.config["checks_enabled"] = {}
        self.config["checks_enabled"][check_name] = enabled
        self.save_config() # حفظ التغيير فوراً
