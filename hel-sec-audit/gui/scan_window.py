# gui/scan_window.py
# This window displays the progress of the security scan.

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QProgressBar
from PyQt5.QtCore import Qt

class ScanWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Scanning System...")
        self.setGeometry(300, 300, 400, 150) # Set initial size
        self.setModal(True) # Make it modal so user can't interact with main window

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)

        self.status_label = QLabel("Initializing scan...")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        layout.addWidget(self.progress_bar)

    def update_progress(self, value, message):
        self.progress_bar.setValue(value)
        self.status_label.setText(message)
        if value == 100:
            self.status_label.setText("Scan Complete!")
