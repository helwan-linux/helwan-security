from PyQt5.QtWidgets import (
    QMainWindow, QVBoxLayout, QPushButton, QLabel, QWidget, 
    QHBoxLayout, QAction
)
from PyQt5.QtGui import QIcon
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

        self.current_theme = "default"
        self.init_ui()
        self.create_menu_bar()
        self.set_theme("default")  # الوضع المبدئي

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        self.app_title_label = QLabel("🔒 hel-sec-audit 🔍")
        self.app_title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.app_title_label)

        main_layout.addStretch()

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

        # قائمة Themes
        theme_menu = menubar.addMenu("Themes")

        dark_theme_action = QAction("🌙 Dark Mode", self)
        dark_theme_action.triggered.connect(lambda: self.set_theme("dark"))
        theme_menu.addAction(dark_theme_action)

        pink_theme_action = QAction("🌸 Pink Mode", self)
        pink_theme_action.triggered.connect(lambda: self.set_theme("pink"))
        theme_menu.addAction(pink_theme_action)

        default_theme_action = QAction("🌤 Default Mode", self)
        default_theme_action.triggered.connect(lambda: self.set_theme("default"))
        theme_menu.addAction(default_theme_action)

    def set_theme(self, theme):
        self.current_theme = theme

        if theme == "dark":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #2e2e2e;
                }
                QMenuBar {
                    background-color: #1c1c1c;
                    color: white;
                }
                QMenuBar::item:selected {
                    background-color: #444;
                }
                QLabel {
                    color: #ddd;
                    font-family: 'Segoe UI';
                    font-size: 24px;
                    font-weight: bold;
                }
                QPushButton {
                    background-color: #444;
                    color: white;
                    border-radius: 10px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #666;
                }
                QPushButton:pressed {
                    background-color: #888;
                }
            """)

        elif theme == "pink":
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #ffe6f0;
                }
                QMenuBar {
                    background-color: #ffb6c1;
                    color: #4b0033;
                }
                QMenuBar::item:selected {
                    background-color: #ff99bb;
                }
                QLabel {
                    color: #99004d;
                    font-family: 'Segoe UI';
                    font-size: 24px;
                    font-weight: bold;
                }
                QPushButton {
                    background-color: #ff5c8a;
                    color: white;
                    border-radius: 10px;
                    padding: 10px 20px;
                }
                QPushButton:hover {
                    background-color: #e6005c;
                }
                QPushButton:pressed {
                    background-color: #cc0052;
                }
            """)

        else:  # Default
            self.setStyleSheet("""
                QMainWindow {
                    background-color: qlineargradient(
                        spread:pad, x1:0, y1:0, x2:1, y2:1,
                        stop:0 #B0B0B0, stop:1 #A0A0A0
                    );
                }
                QMenuBar {
                    background-color: #ddd;
                    color: #222;
                }
                QMenuBar::item:selected {
                    background-color: #bbb;
                }
                QLabel {
                    color: #222;
                    font-family: 'Segoe UI';
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
