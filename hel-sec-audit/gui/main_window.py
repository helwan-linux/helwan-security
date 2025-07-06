# gui/main_window.py
# Contains the main window for the hel-sec-audit application.

from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, 
    QHBoxLayout, QToolButton, QAction # أضف QAction هنا
)
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize

# Import all necessary windows
from gui.scan_window import ScanWindow
from gui.results_window import ResultsWindow
from gui.settings_window import SettingsWindow
from gui.about_window import AboutWindow     

# Import scanner for integration
from core.security_scanner import SecurityScanner


class ScanThread(QThread):
    """
    Thread to run the security scan in the background
    to prevent GUI from freezing.
    """
    progress_updated = pyqtSignal(int, str)
    scan_finished = pyqtSignal(list)

    def __init__(self, scanner):
        super().__init__()
        self.scanner = scanner

    def run(self):
        results = self.scanner.run_all_checks(progress_callback=self.progress_updated.emit)
        self.scan_finished.emit(results)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("hel-sec-audit")
        self.setGeometry(100, 100, 800, 600)

        self.setWindowIcon(QIcon("gui/assets/app_icon.png"))

        self.init_ui()
        self.create_menu_bar() # استدعاء دالة إنشاء شريط القوائم

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        app_title_label = QLabel("<h1>hel-sec-audit</h1>")
        app_title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(app_title_label)

        main_layout.addStretch()

        # هذه الأزرار لم تعد ضرورية هنا لأننا سنستخدم قوائم علوية
        # لإبقاء الكود نظيفًا، سنزيلها
        # Start Scan Button
        # self.start_scan_button = QPushButton("Start Scan")
        # self.start_scan_button.setFixedSize(250, 50)
        # self.start_scan_button.clicked.connect(self.start_scan)
        # button_container_layout.addWidget(self.start_scan_button, alignment=Qt.AlignCenter)

        # Settings Button
        # self.settings_button = QPushButton("Settings")
        # self.settings_button.setFixedSize(250, 50)
        # self.settings_button.clicked.connect(self.open_settings)
        # button_container_layout.addWidget(self.settings_button, alignment=Qt.AlignCenter)

        # About Button (كـ QToolButton مع أيقونة فقط) - سيتم نقله لشريط القوائم/الأدوات
        # self.about_button = QToolButton()
        # self.about_button.setIcon(QIcon("gui/assets/about_icon.png")) 
        # self.about_button.setIconSize(QSize(32, 32)) 
        # self.about_button.setToolTip("About hel-sec-audit")
        # self.about_button.clicked.connect(self.open_about)
        
        # about_button_layout = QHBoxLayout()
        # about_button_layout.addStretch()
        # about_button_layout.addWidget(self.about_button)
        # main_layout.addLayout(about_button_layout)

        # يمكننا إزالة button_container_layout تمامًا إذا لم يعد هناك أزرار هنا
        # main_layout.addLayout(button_container_layout) 

        # إضافة رسالة ترحيب أو تعليمات بسيطة بدلاً من الأزرار
        welcome_label = QLabel("<p align='center'>Please use the menus above to start a scan or configure settings.</p>")
        main_layout.addWidget(welcome_label)


        main_layout.addStretch()
    
    def create_menu_bar(self):
        # إنشاء شريط القوائم العلوي
        menubar = self.menuBar()

        # قائمة File (ملف)
        file_menu = menubar.addMenu("File")
        
        # عمل QAction لـ Exit
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close) # ربط الخروج بالدالة close
        file_menu.addAction(exit_action)

        # قائمة Scan (فحص)
        scan_menu = menubar.addMenu("Scan")
        
        # عمل QAction لـ Start Scan
        start_scan_action = QAction("Start Scan", self)
        start_scan_action.setStatusTip("Begin a new security scan")
        start_scan_action.triggered.connect(self.start_scan)
        scan_menu.addAction(start_scan_action)

        # قائمة Settings (إعدادات)
        settings_menu = menubar.addMenu("Settings")
        
        # عمل QAction لـ Settings
        settings_action = QAction("Application Settings", self)
        settings_action.setStatusTip("Configure application settings")
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)

        # قائمة Help (مساعدة)
        help_menu = menubar.addMenu("Help")
        
        # عمل QAction لـ About
        about_action = QAction(QIcon("gui/assets/about_icon.png"), "About", self) # إضافة الأيقونة هنا
        about_action.setStatusTip("Learn more about hel-sec-audit")
        about_action.triggered.connect(self.open_about)
        help_menu.addAction(about_action)


    def start_scan(self):
        self.scan_win = ScanWindow()
        self.scan_win.show()

        self.scanner = SecurityScanner()

        self.scan_thread = ScanThread(self.scanner)
        self.scan_thread.progress_updated.connect(self.scan_win.update_progress)
        self.scan_thread.scan_finished.connect(self.on_scan_finished)
        self.scan_thread.start()

    def on_scan_finished(self, results):
        self.scan_win.hide()
        self.results_win = ResultsWindow(results)
        self.results_win.show()

    def open_settings(self):
        self.settings_window = SettingsWindow()
        self.settings_window.exec_()

    def open_about(self):
        self.about_window = AboutWindow()
        self.about_window.exec_()
