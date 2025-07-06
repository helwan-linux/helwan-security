import os
from PIL import Image # تأكد من تثبيت Pillow: pip install Pillow

# Define the base directory for the project
PROJECT_ROOT = "hel-sec-audit"

# Define the folder structure
FOLDERS = [
    "gui/assets",
    "core/checks",
    "config",
    "data/reports", # <-- تم إضافة هذا السطر الجديد
    "tests"
]

# Define the files to create with initial content
FILES = {
    # Project root files
    "__init__.py": "# This file makes hel-sec-audit a Python package.",
    "main.py": """# main.py
# This is the main entry point for the hel-sec-audit application.
# It initializes the PyQt5 application and displays the main window.

import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon # تم إضافة هذا الاستيراد
from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Set application icon (for taskbar/window icon)
    # تأكد من أن مسار الأيقونة صحيح
    # If running on Windows, you might prefer .ico. On Linux, .png.
    # قد تحتاج إلى إضافة كود للتعامل مع أيقونات خاصة بنظام التشغيل
    app.setWindowIcon(QIcon("gui/assets/icon.png")) # أو QIcon("gui/assets/icon.ico") لويندوز

    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
""",
    "requirements.txt": """# requirements.txt
# List of Python packages required for this project.
# To install them, run: pip install -r requirements.txt

PyQt5
# reportlab  # For PDF generation (consider alternatives like FPDF if ReportLab is too complex)
# fpdf2      # Another good option for PDF generation
""",
    "README.md": """# hel-sec-audit
## أداة فحص أمان للنظام بالكامل بضغطة واحدة

**الوصف:**
تهدف هذه الأداة إلى فحص الثغرات الأمنية الشائعة في نظام التشغيل (مبدئياً Arch Linux، مع إمكانية العمل على ويندوز).
تقدم الأداة إرشادات بسيطة للمستخدمين لحل هذه الثغرات، وتصدر تقارير PDF جميلة وملونة.

**الميزات:**
* فحص شامل لنقاط الضعف الأمنية الشائعة.
* إرشادات واضحة ومبسطة لحل المشاكل.
* تقارير PDF احترافية وجذابة.
* مصممة خصيصاً للمطورين وباحثي الأمن السيبراني ومحبي الألعاب على Helwan Linux.

**كيفية البدء:**
1.  استنسخ المستودع (clone this repository).
2.  أنشئ بيئة بايثون افتراضية (create a virtual environment).
3.  ثبت المتطلبات: `pip install -r requirements.txt`.
4.  شغل البرنامج: `python main.py`.

**المساهمة:**
نرحب بالمساهمات! يرجى مراجعة ملف `CONTRIBUTING.md` (سيتم إضافته لاحقاً).

**الترخيص:**
هذا المشروع مرخص تحت رخيص [اسم الترخيص، مثال: MIT License]. راجع ملف `LICENSE` للمزيد من التفاصيل.
""",
    "LICENSE": """# MIT License

# حقوق النشر (c) [السنة الحالية] [اسمك أو اسم المؤسسة]

# يُمنح الإذن، مجاناً، لأي شخص يحصل على نسخة من هذا البرنامج والوثائق
# المرتبطة به ("البرنامج")، للتعامل مع البرنامج دون قيود، بما في ذلك
# الحقوق غير المحدودة في استخدام ونسخ وتعديل ودمج ونشر وتوزيع وترخيص فرعي و/أو
# بيع نسخ من البرنامج، والسماح للأشخاص الذين يُقدم لهم البرنامج
# للقيام بذلك، بشرط الالتزام بالشروط التالية:

# إشعار حقوق النشر أعلاه وإشعار الإذن هذا يجب أن يُضمن في جميع النسخ
# أو الأجزاء الجوهرية من البرنامج.

# يُقدم البرنامج "كما هو"، دون أي نوع من الضمان، صريح أو ضمني،
# بما في ذلك، على سبيل المثال لا الحصر، ضمانات صلاحية التسويق،
# والملاءمة لغرض معين، وعدم الانتهاك. لن يكون المؤلفون أو أصحاب حقوق النشر
# مسؤولين بأي حال من الأحوال عن أي مطالبة أو أضرار أو مسؤولية أخرى،
# سواء في دعوى تعاقدية أو ضررية أو غير ذلك، ناشئة عن أو فيما يتعلق
# بالبرنامج أو استخدامه أو التعاملات الأخرى في البرنامج.
""",

    # GUI files
    "gui/__init__.py": "# This makes 'gui' a Python package.",
    "gui/main_window.py": """# gui/main_window.py
# Contains the main window for the hel-sec-audit application.

from PyQt5.QtWidgets import QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, QHBoxLayout # تم إضافة QHBoxLayout
from PyQt5.QtGui import QPixmap, QIcon # For displaying images and icons
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("hel-sec-audit")
        self.setGeometry(100, 100, 800, 600) # Initial window size

        # Set window icon (for taskbar)
        # تأكد من أن مسار الأيقونة صحيح
        self.setWindowIcon(QIcon("gui/assets/icon.png")) # أو QIcon("gui/assets/icon.ico") لويندوز

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Logo display
        # عرض الشعار في واجهة المستخدم
        logo_label = QLabel(self)
        pixmap = QPixmap("gui/assets/logo.png") # تأكد من وجود ملف الشعار
        if not pixmap.isNull():
            # قم بتحجيم الصورة لتناسب الواجهة بشكل جيد
            logo_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)
        else:
            print("Error: logo.png not found or could not be loaded. Displaying placeholder text.")
            # يمكنك عرض رسالة خطأ أو نص بديل هنا
            temp_logo_label = QLabel("hel-sec-audit")
            temp_logo_label.setAlignment(Qt.AlignCenter)
            temp_logo_label.setStyleSheet("font-size: 36px; font-weight: bold;")
            layout.addWidget(temp_logo_label)


        # Add spacing
        layout.addStretch()

        # Start Scan Button
        self.start_scan_button = QPushButton("Start Scan")
        self.start_scan_button.clicked.connect(self.start_scan)
        layout.addWidget(self.start_scan_button)

        # Settings Button
        self.settings_button = QPushButton("Settings")
        self.settings_button.clicked.connect(self.open_settings)
        layout.addWidget(self.settings_button)

        # About Button
        self.about_button = QPushButton("About")
        self.about_button.clicked.connect(self.open_about)
        layout.addWidget(self.about_button)

        # Add spacing
        layout.addStretch()

    def start_scan(self):
        # Placeholder for starting the scan
        # هنا سيتم استدعاء شاشة الفحص الجاري وبدء عملية الفحص الفعلية
        print("Starting security scan...")
        # Example: self.scan_window = ScanWindow(); self.scan_window.show()

    def open_settings(self):
        # Placeholder for opening settings window
        # هنا سيتم فتح شاشة الإعدادات
        print("Opening settings...")
        # Example: self.settings_window = SettingsWindow(); self.settings_window.show()

    def open_about(self):
        # Placeholder for opening about window
        # هنا سيتم فتح شاشة "حول البرنامج"
        print("Opening about window...")
        # Example: self.about_window = AboutWindow(); self.about_window.show()
""",
    "gui/scan_window.py": """# gui/scan_window.py
# This window displays the progress of the security scan.

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar

class ScanWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scanning System...")
        self.setGeometry(200, 200, 400, 200)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.status_label = QLabel("Initializing scan...")
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100) # Percentage progress
        layout.addWidget(self.progress_bar)

        # Example: update_progress(50, "Checking for updates...")
        # هذا مثال لكيفية تحديث شريط التقدم والرسالة
    
    def update_progress(self, percentage, message):
        self.progress_bar.setValue(percentage)
        self.status_label.setText(message)
""",
    "gui/results_window.py": """# gui/results_window.py
# This window displays the final scan results and options to generate a report.

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QPushButton, QScrollArea, QWidget, QHBoxLayout # تم إضافة QHBoxLayout

class ResultsWindow(QDialog):
    def __init__(self, scan_results): # scan_results will be a list of dictionaries/objects
        super().__init__()
        self.setWindowTitle("Scan Results")
        self.setGeometry(150, 150, 900, 700)
        self.scan_results = scan_results # Store the results

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Summary
        summary_label = QLabel("<h2>Scan Summary</h2>")
        main_layout.addWidget(summary_label)

        # Example summary (you'll populate this dynamically)
        # مثال لملخص النتائج (سيتم ملؤه ديناميكياً)
        issues_count = sum(1 for r in self.scan_results if not r.get('is_secure', True)) # افتراض أن is_secure تدل على عدم وجود مشكلة
        total_checks = len(self.scan_results)
        summary_text = f"<p>Total checks performed: <b>{total_checks}</b></p>"
        summary_text += f"<p>Issues found: <b style='color: {'red' if issues_count > 0 else 'green'};'>{issues_count}</b></p>"
        main_layout.addWidget(QLabel(summary_text))

        # Detailed Results (Scrollable)
        details_label = QLabel("<h2>Detailed Findings</h2>")
        main_layout.addWidget(details_label)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        content_widget = QWidget()
        scroll_area.setWidget(content_widget)
        details_layout = QVBoxLayout(content_widget)

        # Populate with actual results
        # ملء القائمة بالنتائج الفعلية
        for result in self.scan_results:
            # Example structure: {'check_name': 'System Updates', 'is_secure': False, 'severity': 'High', 'description': 'Your system is not up-to-date.', 'solution': 'Run sudo apt update && sudo apt upgrade'}
            status_color = 'green' if result.get('is_secure', True) else 'red'
            severity_color = 'darkred' if result.get('severity', 'Low') == 'High' else ('orange' if result.get('severity') == 'Medium' else 'darkgreen')

            item_text = f"<p><b>Check:</b> {result.get('check_name', 'N/A')}</p>"
            item_text += f"<p><b>Status:</b> <span style='color: {status_color};'>{'Secure' if result.get('is_secure', True) else 'Vulnerable'}</span> (Severity: <span style='color: {severity_color};'>{result.get('severity', 'N/A')}</span>)</p>"
            item_text += f"<p><b>Description:</b> {result.get('description', 'No description.')}</p>"
            item_text += f"<p><b>Solution:</b> {result.get('solution', 'No solution provided.')}</p>"
            item_text += "<hr>" # Separator for better readability
            
            details_layout.addWidget(QLabel(item_text))

        main_layout.addWidget(scroll_area)

        # Generate PDF Report Button
        self.generate_report_button = QPushButton("Generate PDF Report")
        self.generate_report_button.clicked.connect(self.generate_pdf_report)
        main_layout.addWidget(self.generate_report_button)

    def generate_pdf_report(self):
        # Placeholder for PDF generation
        # هنا سيتم استدعاء الدالة المسؤولة عن توليد تقرير PDF
        print("Generating PDF report...")
        # Example: from core.report_generator import ReportGenerator
        # ReportGenerator.generate(self.scan_results)
""",
    "gui/settings_window.py": """# gui/settings_window.py
# This window allows users to configure application settings.

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QCheckBox, QLineEdit, QPushButton, QFileDialog, QHBoxLayout # تم إضافة QHBoxLayout

class SettingsWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Settings")
        self.setGeometry(250, 250, 500, 300)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        layout.addWidget(QLabel("<h2>Scan Preferences</h2>"))

        # Example: Checkbox for specific scan types
        # مثال: صندوق اختيار لأنواع فحص محددة
        self.scan_updates_checkbox = QCheckBox("Scan for System Updates")
        self.scan_updates_checkbox.setChecked(True) # Default value
        layout.addWidget(self.scan_updates_checkbox)

        self.scan_ports_checkbox = QCheckBox("Scan for Open Ports")
        self.scan_ports_checkbox.setChecked(True)
        layout.addWidget(self.scan_ports_checkbox)

        layout.addWidget(QLabel("<h2>Report Settings</h2>"))

        # Report output path
        # مسار حفظ التقارير
        self.report_path_label = QLabel("Report Output Path:")
        layout.addWidget(self.report_path_label)

        path_layout = QHBoxLayout() # Requires from PyQt5.QtWidgets import QHBoxLayout
        self.report_path_lineEdit = QLineEdit("data/reports/") # Default path
        path_layout.addWidget(self.report_path_lineEdit)

        self.browse_button = QPushButton("Browse...")
        self.browse_button.clicked.connect(self.browse_for_path)
        path_layout.addWidget(self.browse_button)
        layout.addLayout(path_layout)

        # Save Settings Button
        self.save_button = QPushButton("Save Settings")
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

    def browse_for_path(self):
        # Open a folder dialog to select report output path
        # فتح مربع حوار لتحديد مجلد حفظ التقارير
        folder_path = QFileDialog.getExistingDirectory(self, "Select Report Output Folder")
        if folder_path:
            self.report_path_lineEdit.setText(folder_path)

    def save_settings(self):
        # Placeholder for saving settings
        # هنا يتم حفظ الإعدادات (مثلاً في ملف JSON أو عبر مكتبة configparser)
        print("Settings saved!")
        # Example: Save self.scan_updates_checkbox.isChecked(), self.report_path_lineEdit.text()
        self.accept() # Close the dialog
""",
    "gui/about_window.py": """# gui/about_window.py
# This window displays information about the application.

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPixmap # For displaying images
from PyQt5.QtCore import Qt # تم إضافة هذا الاستيراد

class AboutWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About hel-sec-audit")
        self.setGeometry(300, 300, 400, 300)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Logo display (smaller version)
        # عرض الشعار في شاشة "حول"
        logo_label = QLabel(self)
        pixmap = QPixmap("gui/assets/logo.png") # تأكد من وجود ملف الشعار
        if not pixmap.isNull():
            logo_label.setPixmap(pixmap.scaled(100, 100, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            logo_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(logo_label)

        layout.addWidget(QLabel("<h2 align='center'>hel-sec-audit</h2>"))
        layout.addWidget(QLabel("<p align='center'>Version: 0.1.0</p>"))
        layout.addWidget(QLabel("<p align='center'>Developed by: [Your Name/Team Name]</p>"))
        layout.addWidget(QLabel("<p align='center'>© 2025 All rights reserved.</p>"))
        layout.addWidget(QLabel("<p align='center'>This tool is designed to enhance the security posture of your system.</p>"))

        # Add some spacing
        layout.addStretch()

        # Close button
        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept) # Closes the dialog
        layout.addWidget(close_button)
""",

    # Core files
    "core/__init__.py": "# This makes 'core' a Python package.",
    "core/security_scanner.py": """# core/security_scanner.py
# Main class for orchestrating security checks.

from core.checks.system_updates import SystemUpdatesCheck
from core.checks.open_ports import OpenPortsCheck
from core.checks.weak_passwords import WeakPasswordsCheck # تم إضافة هذا الاستيراد
from core.checks.firewall_status import FirewallStatusCheck # تم إضافة هذا الاستيراد
# Import other checks as you create them

class SecurityScanner:
    def __init__(self):
        # List of security check modules to run
        # قائمة بوحدات فحص الأمان التي سيتم تشغيلها
        self.checks = [
            SystemUpdatesCheck(),
            WeakPasswordsCheck(), # أضف الفحص هنا
            OpenPortsCheck(),
            FirewallStatusCheck(), # أضف الفحص هنا
            # أضف المزيد من فحوصات الأمان هنا
        ]
        self.results = []

    def run_all_checks(self, progress_callback=None):
        # Runs all defined security checks.
        # تقوم بتشغيل جميع فحوصات الأمان المعرفة.
        self.results = []
        total_checks = len(self.checks)
        for i, check in enumerate(self.checks):
            current_progress = int(((i + 1) / total_checks) * 100)
            status_message = f"Running check: {check.__class__.__name__.replace('Check', '')}..."
            
            if progress_callback:
                progress_callback(current_progress, status_message)
            
            print(f"Running: {check.__class__.__name__}") # For console output
            
            # Execute the check and get its result
            # تنفيذ الفحص والحصول على نتيجته
            result = check.run_check()
            self.results.append(result)
        
        return self.results

    def get_results(self):
        # Returns the collected scan results.
        # تعيد نتائج الفحص المجمعة.
        return self.results
""",
    "core/report_generator.py": """# core/report_generator.py
# This module is responsible for generating beautiful and colorful PDF reports.

# You will need to install a PDF generation library like ReportLab or FPDF2.
# على سبيل المثال، باستخدام ReportLab:
# from reportlab.lib.pagesizes import letter
# from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
# from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
# from reportlab.lib.enums import TA_CENTER, TA_LEFT
# from reportlab.lib.colors import green, red, orange, black
# from reportlab.lib.units import inch # تم إضافة هذا الاستيراد

import os
from datetime import datetime

class ReportGenerator:
    @staticmethod
    def generate(scan_results, output_path="data/reports/security_report.pdf"):
        # Generates a PDF report from scan results.
        # تقوم بتوليد تقرير PDF من نتائج الفحص.

        # Ensure output directory exists
        # التأكد من وجود مجلد الإخراج
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # Placeholder for PDF generation logic
        # هذا مكان منطق توليد ملف PDF الفعلي
        print(f"Placeholder: Generating PDF report at {output_path}")
        print("Scan Results for report:", scan_results)

        # Example with a basic text file for now
        # مثال بملف نصي بسيط الآن (يمكن استبداله لاحقاً بـ PDF فعلي)
        text_report_path = output_path.replace('.pdf', '.txt')
        with open(text_report_path, 'w', encoding='utf-8') as f:
            f.write("hel-sec-audit Security Report\\n")
            f.write("-------------------------------------\\n")
            f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\\n\\n")
            f.write("Scan Summary:\\n")
            issues_count = sum(1 for r in scan_results if not r.get('is_secure', True))
            total_checks = len(scan_results)
            f.write(f"Total checks performed: {total_checks}\\n")
            f.write(f"Issues found: {issues_count}\\n\\n")

            f.write("Detailed Findings:\\n")
            for result in scan_results:
                f.write(f"-------------------------------------\\n")
                f.write(f"Check: {result.get('check_name', 'N/A')}\\n")
                f.write(f"Status: {'Secure' if result.get('is_secure', True) else 'Vulnerable'}\\n")
                f.write(f"Severity: {result.get('severity', 'N/A')}\\n")
                f.write(f"Description: {result.get('description', 'No description.')}\\n")
                f.write(f"Solution: {result.get('solution', 'No solution provided.')}\\n\\n")

        print(f"Basic text report generated at {text_report_path}. Replace with actual PDF generation code.")

        # To implement actual PDF generation using ReportLab:
        # doc = SimpleDocTemplate(output_path, pagesize=letter)
        # styles = getSampleStyleSheet()
        # story = []
        #
        # # Add logo (optional)
        # try:
        #     logo = Image("gui/assets/logo.png")
        #     logo.width = 100
        #     logo.height = 100
        #     story.append(logo)
        #     story.append(Spacer(1, 0.2 * inch))
        # except Exception as e:
        #     print(f"Could not load logo for report: {e}")
        #
        # # Title
        # title_style = ParagraphStyle('Title', parent=styles['h1'], alignment=TA_CENTER, fontSize=24, spaceAfter=14)
        # story.append(Paragraph("hel-sec-audit Security Report", title_style))
        # story.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        # story.append(Spacer(1, 0.2 * inch))
        #
        # # Summary
        # story.append(Paragraph("<h2>Scan Summary</h2>", styles['h2']))
        # issues_count = sum(1 for r in scan_results if not r.get('is_secure', True))
        # total_checks = len(scan_results)
        # story.append(Paragraph(f"Total checks performed: <b>{total_checks}</b>", styles['Normal']))
        # story.append(Paragraph(f"Issues found: <font color='{'red' if issues_count > 0 else 'green'}'><b>{issues_count}</b></font>", styles['Normal']))
        # story.append(Spacer(1, 0.2 * inch))
        #
        # # Detailed Findings
        # story.append(Paragraph("<h2>Detailed Findings</h2>", styles['h2']))
        # for result in scan_results:
        #     status_color = green if result.get('is_secure', True) else red
        #     severity_color = red if result.get('severity', 'Low') == 'High' else (orange if result.get('severity') == 'Medium' else green)
        #
        #     story.append(Paragraph(f"<b>Check:</b> {result.get('check_name', 'N/A')}", styles['Normal']))
        #     story.append(Paragraph(f"<b>Status:</b> <font color='{status_color}'>{'Secure' if result.get('is_secure', True) else 'Vulnerable'}</font> (Severity: <font color='{severity_color}'>{result.get('severity', 'N/A')}</font>)", styles['Normal']))
        #     story.append(Paragraph(f"<b>Description:</b> {result.get('description', 'No description.')}", styles['Normal']))
        #     story.append(Paragraph(f"<b>Solution:</b> {result.get('solution', 'No solution provided.')}", styles['Normal']))
        #     story.append(Spacer(1, 0.1 * inch))
        #     from reportlab.platypus import HRFlowable # Import if not already done
        #     story.append(HRFlowable(width="100%", thickness=1, lineCap='round', color=black, spaceBefore=6, spaceAfter=6))
        #     story.append(Spacer(1, 0.1 * inch))
        #
        # doc.build(story)
        # print(f"PDF report generated successfully at {output_path}")

""",
    "core/utils.py": """# core/utils.py
# Contains utility functions used across the application.

import subprocess
import platform

def run_command(command_parts, sudo_required=False):
    # Runs a shell command and returns its output and error.
    # If sudo_required is True, it will attempt to run with sudo on Linux/macOS.
    # تقوم بتشغيل أمر shell وتعيد مخرجاته وأخطائه.
    # إذا كانت sudo_required صحيحة، فستحاول التشغيل باستخدام sudo على Linux/macOS.
    try:
        # Handle sudo on Linux/macOS
        # التعامل مع sudo على Linux/macOS
        if sudo_required and platform.system() != "Windows":
            command_parts = ["sudo"] + command_parts
            # For Windows, running as admin is usually done by launching the script
            # with elevated privileges, not by prefixing commands with 'sudo'.
            # لويندوز، عادة ما يتم تشغيل كمسؤول عن طريق تشغيل السكريبت بامتيازات مرتفعة.

        # Use subprocess.run for safer command execution
        # استخدام subprocess.run لتنفيذ الأوامر بشكل أكثر أماناً
        result = subprocess.run(
            command_parts,
            capture_output=True,
            text=True, # Decode stdout/stderr as text
            check=False # Do not raise exception for non-zero exit codes
        )
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except FileNotFoundError:
        return "", f"Error: Command '{command_parts[0]}' not found.", 1
    except Exception as e:
        return "", f"An unexpected error occurred: {e}", 1

def is_linux():
    # Checks if the current operating system is Linux.
    # تتحقق مما إذا كان نظام التشغيل الحالي هو Linux.
    return platform.system() == "Linux"

def is_windows():
    # Checks if the current operating system is Windows.
    # تتحقق مما إذا كان نظام التشغيل الحالي هو Windows.
    return platform.system() == "Windows"

# Add more utility functions here (e.g., file permission checks, network checks)
# أضف المزيد من دوال المساعدة هنا (مثل فحص أذونات الملفات، فحوصات الشبكة)
""",

    # Core checks files
    "core/checks/__init__.py": "# This makes 'checks' a Python package.",
    "core/checks/system_updates.py": """# core/checks/system_updates.py
# Checks if the system has pending security updates.

from core.utils import run_command, is_linux, is_windows

class SystemUpdatesCheck:
    def __init__(self):
        self.check_name = "System Updates Status"
        self.description = "Checks if your operating system has all the latest security updates installed."
        self.solution = "Run system update commands (e.g., 'sudo apt update && sudo apt upgrade' on Debian/Ubuntu, or use 'pacman -Syu' on Arch Linux). For Windows, check 'Windows Update' settings."
        self.severity = "High" # Default severity

    def run_check(self):
        # Runs the check based on the operating system.
        # تقوم بتشغيل الفحص بناءً على نظام التشغيل.
        if is_linux():
            return self._check_linux_updates()
        elif is_windows():
            return self._check_windows_updates()
        else:
            return self._create_result(False, "Unsupported OS", "The current operating system is not supported for this check.", "Install updates manually if available.", "Medium")

    def _check_linux_updates(self):
        # Placeholder for Linux update check (e.g., Arch Linux specific)
        # هذا مكان فحص تحديثات Linux (خاصة بـ Arch Linux)
        # For Arch Linux: `pacman -Qu` (queries for outdated packages)
        # For Debian/Ubuntu: `sudo apt update && apt list --upgradable`
        
        # This is a dummy check for now. You'll replace it with actual commands.
        # هذا فحص وهمي الآن. ستقوم باستبداله بأوامر فعلية.
        stdout, stderr, return_code = run_command(["echo", "Simulating update check..."])
        
        # Example for Arch Linux:
        # stdout, stderr, return_code = run_command(["pacman", "-Qu"])
        # if return_code == 0 and not stdout: # No outdated packages
        #     return self._create_result(True, "System is up-to-date", "No pending updates found.", "N/A", "Low")
        # elif return_code == 0 and stdout: # Outdated packages found
        #     return self._create_result(False, "Pending system updates", "Your system has pending updates that may include security patches.", self.solution, "High")
        # else:
        #     return self._create_result(False, "Update check failed", f"Could not check for updates: {stderr}", self.solution, "Medium")

        # Dummy result: assume updates are needed
        return self._create_result(False, "Pending system updates (Simulated)", "Your system has pending updates that may include security patches.", self.solution, "High")


    def _check_windows_updates(self):
        # Placeholder for Windows update check
        # هذا مكان فحص تحديثات Windows
        # This is more complex and usually involves PowerShell cmdlets or WMI.
        # يمكن استخدام PowerShell cmdlets مثل Get-WindowsUpdate.
        return self._create_result(False, "Windows updates status (Simulated)", "Checking Windows updates is complex programmatically.", "Check Windows Update settings manually.", "Medium")

    def _create_result(self, is_secure, title, description, solution, severity):
        # Helper to format the result.
        # دالة مساعدة لتنسيق النتيجة.
        return {
            "check_name": self.check_name,
            "is_secure": is_secure,
            "title": title,
            "description": description,
            "solution": solution,
            "severity": severity
        }
""",
    "core/checks/weak_passwords.py": """# core/checks/weak_passwords.py
# Checks for weak password policies or common weak passwords (requires elevated privileges).

from core.utils import run_command, is_linux, is_windows

class WeakPasswordsCheck:
    def __init__(self):
        self.check_name = "Weak Password Policies/Usage"
        self.description = "Assesses system password policies or identifies accounts with common weak passwords."
        self.solution = "Ensure strong password policies are enforced (e.g., minimum length, complexity requirements). Avoid common or easily guessable passwords. Change any identified weak passwords immediately."
        self.severity = "High"

    def run_check(self):
        # This check is complex and might require elevated privileges and careful implementation.
        # هذا الفحص معقد وقد يتطلب امتيازات مرتفعة وتنفيذ دقيق.
        if is_linux():
            return self._check_linux_passwords()
        elif is_windows():
            return self._check_windows_passwords()
        else:
            return self._create_result(True, "Unsupported OS", "Password check not supported on this OS.", "N/A", "Low")

    def _check_linux_passwords(self):
        # Placeholder for Linux password check.
        # This could involve parsing /etc/login.defs for password policy settings,
        # or (with extreme caution and user consent) checking against a list of common weak passwords.
        # هذا المكان لفحص كلمات المرور في Linux.
        # يمكن أن يتضمن تحليل ملفات مثل /etc/login.defs لسياسات كلمات المرور،
        # أو (بحذر شديد وبموافقة المستخدم) التحقق من قائمة كلمات المرور الشائعة الضعيفة.
        
        # For demonstration, let's assume it finds a weak policy.
        # لأغراض التوضيح، لنفترض أنه يجد سياسة ضعيفة.
        return self._create_result(False, "Weak password policy detected (Simulated)", "System password policy may be too lenient.", self.solution, "High")

    def _check_windows_passwords(self):
        # Placeholder for Windows password check.
        # This might involve querying Active Directory or local security policies.
        # هذا المكان لفحص كلمات المرور في Windows.
        # قد يتضمن الاستعلام عن Active Directory أو سياسات الأمان المحلية.
        return self._create_result(True, "Windows password policy (Simulated)", "Windows password policy seems okay.", "N/A", "Low")

    def _create_result(self, is_secure, title, description, solution, severity):
        return {
            "check_name": self.check_name,
            "is_secure": is_secure,
            "title": title,
            "description": description,
            "solution": solution,
            "severity": severity
        }
""",
    "core/checks/open_ports.py": """# core/checks/open_ports.py
# Checks for unexpectedly open network ports.

import socket
from core.utils import is_linux, is_windows

class OpenPortsCheck:
    def __init__(self):
        self.check_name = "Open Network Ports"
        self.description = "Identifies network ports that are open and listening, which could be exploited if not properly secured."
        self.solution = "Close unnecessary open ports using your system's firewall (e.g., UFW on Linux, Windows Defender Firewall). Ensure only essential services are exposed."
        self.severity = "Medium"
        # List of common ports to check. Extend this as needed.
        # قائمة بالمنافذ الشائعة للفحص. قم بتوسيعها حسب الحاجة.
        self.ports_to_check = [21, 22, 23, 80, 443, 3389] # FTP, SSH, Telnet, HTTP, HTTPS, RDP

    def run_check(self):
        # Runs the port check.
        # تقوم بتشغيل فحص المنفذ.
        open_ports_found = []
        for port in self.ports_to_check:
            if self._is_port_open("127.0.0.1", port): # Check localhost
                open_ports_found.append(port)
            # You might want to also check external IP, but that requires more setup
            # قد ترغب أيضاً في فحص IP خارجي، لكن ذلك يتطلب المزيد من الإعداد

        if open_ports_found:
            return self._create_result(False, "Open ports detected", f"The following ports are open: {', '.join(map(str, open_ports_found))}. These could be entry points for attackers.", self.solution, "High")
        else:
            return self._create_result(True, "No obvious open ports", "No commonly exploited ports were found to be unexpectedly open.", "N/A", "Low")

    def _is_port_open(self, host, port):
        # Checks if a specific port on a given host is open.
        # تتحقق مما إذا كان منفذ معين على مضيف معين مفتوحاً.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5) # Short timeout
        try:
            s.connect((host, port))
            return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            return False
        finally:
            s.close()

    def _create_result(self, is_secure, title, description, solution, severity):
        return {
            "check_name": self.check_name,
            "is_secure": is_secure,
            "title": title,
            "description": description,
            "solution": solution,
            "severity": severity
        }
""",
    "core/checks/firewall_status.py": """# core/checks/firewall_status.py
# Checks the status of the system's firewall.

from core.utils import run_command, is_linux, is_windows

class FirewallStatusCheck:
    def __init__(self):
        self.check_name = "Firewall Status"
        self.description = "Verifies if the system's firewall is active and configured to protect against unauthorized access."
        self.solution = "Enable your system's firewall (e.g., UFW on Linux, Windows Defender Firewall) and ensure it's configured to block unnecessary incoming connections."
        self.severity = "High"

    def run_check(self):
        # Runs the check based on the operating system.
        # تقوم بتشغيل الفحص بناءً على نظام التشغيل.
        if is_linux():
            return self._check_linux_firewall()
        elif is_windows():
            return self._check_windows_firewall()
        else:
            return self._create_result(False, "Unsupported OS", "Firewall check not supported on this OS.", "N/A", "Low")

    def _check_linux_firewall(self):
        # Checks UFW (Uncomplicated Firewall) status on Linux (common for Arch/Ubuntu).
        # تتحقق من حالة UFW (جدار الحماية غير المعقد) على Linux (شائع لـ Arch/Ubuntu).
        stdout, stderr, return_code = run_command(["sudo", "ufw", "status"], sudo_required=True)
        if "Status: active" in stdout:
            return self._create_result(True, "Firewall is active", "UFW is running and providing basic protection.", "N/A", "Low")
        elif "Status: inactive" in stdout:
            return self._create_result(False, "Firewall is inactive", "UFW is not active, leaving your system exposed.", self.solution, "High")
        else:
            return self._create_result(False, "Could not determine firewall status", f"Error checking UFW: {stderr}", self.solution, "Medium")

    def _check_windows_firewall(self):
        # Checks Windows Defender Firewall status using PowerShell.
        # تتحقق من حالة Windows Defender Firewall باستخدام PowerShell.
        # This command requires PowerShell and usually admin privileges.
        # هذا الأمر يتطلب PowerShell وامتيازات المسؤول عادة.
        cmd = ["powershell", "-Command", "(Get-NetFirewallProfile -Name Domain,Private,Public).Enabled | Select-Object -Unique"]
        stdout, stderr, return_code = run_command(cmd) # sudo_required not strictly needed as elevation handles it on Windows

        if "True" in stdout: # All profiles active
            return self._create_result(True, "Windows Firewall is active", "Windows Defender Firewall is running.", "N/A", "Low")
        elif "False" in stdout:
            return self._create_result(False, "Windows Firewall is inactive", "Windows Defender Firewall is not active, leaving your system exposed.", self.solution, "High")
        else:
            return self._create_result(False, "Could not determine Windows Firewall status", f"Error checking Windows Firewall: {stderr}", self.solution, "Medium")

    def _create_result(self, is_secure, title, description, solution, severity):
        return {
            "check_name": self.check_name,
            "is_secure": is_secure,
            "title": title,
            "description": description,
            "solution": solution,
            "severity": severity
        }
""",

    # Config files
    "config/__init__.py": "# This makes 'config' a Python package.",
    "config/settings.py": """# config/settings.py
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

""",
    "config/messages.py": """# config/messages.py
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
""",

    # Data files
    "data/__init__.py": "# This makes 'data' a Python package."
    # تم إزالة "data/reports/.gitkeep" من هنا لأن المجلد "data/reports" سيتم إنشاؤه مسبقاً.
    # يمكنك إضافة هذا الملف يدوياً بعد تشغيل السكريبت إذا أردت التأكد من تتبع Git للمجلد الفارغ.
}

def create_project_structure():
    """
    Creates the folder and file structure for the hel-sec-audit project.
    تقوم بإنشاء هيكل المجلدات والملفات لمشروع hel-sec-audit.
    """
    if os.path.exists(PROJECT_ROOT):
        print(f"Warning: Project folder '{PROJECT_ROOT}' already exists. Skipping creation of existing folders/files.")
    else:
        os.makedirs(PROJECT_ROOT)
        print(f"Created project root folder: {PROJECT_ROOT}/")

    original_cwd = os.getcwd() # Keep track of original working directory
    os.chdir(PROJECT_ROOT) # Change current directory to project root

    # Create folders
    for folder in FOLDERS:
        os.makedirs(folder, exist_ok=True)
        print(f"Created folder: {PROJECT_ROOT}/{folder}/")

    # Create files with initial content
    for file_path, content in FILES.items():
        file_full_path = os.path.join(file_path)

        # Handle special case for gui/assets, ensure images exist or are created as placeholders
        if file_path.startswith("gui/assets/") and (file_path.endswith(".png") or file_path.endswith(".ico")):
            if not os.path.exists(file_full_path):
                # Only create image placeholder if Pillow is available
                if 'Image' in globals(): # Check if PIL.Image was imported successfully
                    img = Image.new('RGB', (100, 100), color = 'red')
                    img.save(file_full_path)
                    print(f"Created placeholder image: {PROJECT_ROOT}/{file_full_path}")
                else:
                    print(f"Skipping creation of image {file_full_path} as Pillow is not installed.")
            continue # Skip writing text content for image files

        # Create other text files if they don't exist
        if not os.path.exists(file_full_path):
            with open(file_full_path, "w", encoding="utf-8") as f:
                f.write(content.strip())
            print(f"Created file: {PROJECT_ROOT}/{file_full_path}")
        else:
            print(f"File already exists: {PROJECT_ROOT}/{file_full_path}. Skipping content overwrite.")
    
    # Optional: Create .gitkeep in data/reports if needed for git
    gitkeep_path = os.path.join("data", "reports", ".gitkeep")
    if not os.path.exists(gitkeep_path):
        with open(gitkeep_path, "w") as f:
            f.write("# This file is here to ensure the 'reports' directory is kept by Git.\n")
        print(f"Created file: {PROJECT_ROOT}/{gitkeep_path}")


    os.chdir(original_cwd) # Change back to original working directory
    print("\\nProject structure created successfully!")
    print(f"To start, navigate to the '{PROJECT_ROOT}' directory and run 'python main.py'")
    print(f"Remember to install dependencies: 'pip install -r requirements.txt'")

if __name__ == "__main__":
    try:
        # Check if Pillow is installed for placeholder images
        from PIL import Image
        print("Pillow library found. Placeholder images will be created.")
    except ImportError:
        print("Pillow library not found. Please install it using 'pip install Pillow' to create placeholder images.")
        print("Continuing without creating placeholder image files.")
        # Make Image unavailable globally if not imported
        Image = None
    
    create_project_structure()
