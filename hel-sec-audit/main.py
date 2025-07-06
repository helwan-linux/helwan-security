import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)

    icon = QIcon("/usr/share/pixmaps/hel-sec-audit.png")
    app.setWindowIcon(icon)

    main_win = MainWindow()
    main_win.setWindowIcon(icon)
    main_win.show()

    sys.exit(app.exec_())
