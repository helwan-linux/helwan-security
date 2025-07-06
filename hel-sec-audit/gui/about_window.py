# gui/about_window.py
# This window displays information about the application.

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

class AboutWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About hel-sec-audit")
        self.setGeometry(300, 300, 400, 300)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # اللوجو الصغير في شاشة "حول البرنامج" (يمكنك الاحتفاظ به أو إزالته حسب الرغبة)
        # إذا كنت لا تريد اللوجو هنا أيضًا، قم بإزالة الأسطر التالية
        logo_label = QLabel(self)
        pixmap = QPixmap("gui/assets/logo.png") # تأكد من وجود ملف الشعار
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)

        layout.addWidget(QLabel("<h2 align='center'>hel-sec-audit</h2>"))
        layout.addWidget(QLabel("<p align='center'>Version: 0.1.0</p>"))
        layout.addWidget(QLabel("<p align='center'>Developed by: [Saeed Badrelden]</p>"))
        layout.addWidget(QLabel("<p align='center'>E-MAIL: [saeedbadrelden2021@gmail.com]</p>"))
        layout.addWidget(QLabel("<p align='center'>© 2025 All rights reserved.</p>"))
        layout.addWidget(QLabel("<p align='center'>This tool is designed to enhance the security posture of your system.</p>"))

        # Add some spacing
        layout.addStretch()

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)
