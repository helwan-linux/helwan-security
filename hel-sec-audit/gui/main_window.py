from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, 
    QHBoxLayout, QToolButton, QAction
)
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize

# Import all necessary windows
from gui.scan_window import ScanWindow
from gui.results_window import ResultsWindow
from gui.settings_window import SettingsWindow
from gui.about_window import AboutWindow     

# Import scanner
from core.security_scanner import SecurityScanner


class ScanThread(QThread):
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

        # تعيين الألوان والتصميم العام
        self.setStyleSheet("""
            QMainWindow {
                background-color: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #B0B0B0, stop:1 #A0A0A0
                );
            }

            QLabel {
                color: #222;
                font-family: 'Segoe UI', 'Arial';
                font-size: 24px;
                font-weight: bold;
            }

            QPushButton {
                background-color: #3a7bd5;
                color: white;
                border: none;
                padding: 12px 24px;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
                font-family: 'Segoe UI';
            }

            QPushButton:hover {
                background-color: #285ea8;
            }

            QPushButton:pressed {
                background-color: #1e4a8a;
            }
        """)

        self.init_ui()
        self.create_menu_bar()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        app_title_label = QLabel("🔒 hel-sec-audit 🔍")
        app_title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(app_title_label)

        main_layout.addStretch()

        # زر Start Scan في منتصف الشاشة
        self.start_scan_button = QPushButton("🚀 Start Scan")
        self.start_scan_button.setFixedSize(250, 50)
        self.start_scan_button.clicked.connect(self.start_scan)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(self.start_scan_button)
        button_layout.addStretch()

        main_layout.addLayout(button_layout)

        main_layout.addStretch()

    def create_menu_bar(self):
        menubar = self.menuBar()

        # قائمة File
        file_menu = menubar.addMenu("File")
        exit_action = QAction("Exit", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.setStatusTip("Exit the application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # قائمة Settings
        settings_menu = menubar.addMenu("Settings")
        settings_action = QAction("Application Settings", self)
        settings_action.setStatusTip("Configure application settings")
        settings_action.triggered.connect(self.open_settings)
        settings_menu.addAction(settings_action)

        # قائمة Help
        help_menu = menubar.addMenu("Help")
        about_action = QAction(QIcon("gui/assets/about_icon.png"), "About", self)
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
