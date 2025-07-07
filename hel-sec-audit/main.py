import os
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    base_path = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_path, "gui", "assets", "app_icon.png")
    app.setWindowIcon(QIcon(icon_path))

    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
