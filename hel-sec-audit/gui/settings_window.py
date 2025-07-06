# gui/settings_window.py
# This window will handle application settings.

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QCheckBox, QGroupBox, QFormLayout
from PyQt5.QtCore import Qt

from core.config_manager import ConfigManager

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(200, 200, 500, 400) 

        self.config_manager = ConfigManager()
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(QLabel("<h1>Application Settings</h1>"))
        
        checks_group_box = QGroupBox("Enable/Disable Security Checks")
        checks_layout = QVBoxLayout()
        checks_group_box.setLayout(checks_layout)
        
        self.check_boxes = {}
        
        current_check_settings = self.config_manager.get_all_check_settings()

        check_names = [
            "System Updates Status",
            "Weak Password Policies/Usage",
            "Open Network Ports",
            "Firewall Status",
            "Antivirus Status",
            "Browser Security Settings",
            "Installed Software Updates" # <--- إضافة اسم الفحص الجديد هنا
        ]

        for check_name in check_names:
            checkbox = QCheckBox(check_name)
            checkbox.setChecked(current_check_settings.get(check_name, True))
            checkbox.stateChanged.connect(lambda state, name=check_name: self._save_check_setting(name, state))
            checks_layout.addWidget(checkbox)
            self.check_boxes[check_name] = checkbox

        main_layout.addWidget(checks_group_box)

        main_layout.addStretch()

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        main_layout.addWidget(close_button)

    def _save_check_setting(self, check_name, state):
        is_enabled = bool(state == Qt.Checked)
        self.config_manager.set_check_enabled(check_name, is_enabled)
