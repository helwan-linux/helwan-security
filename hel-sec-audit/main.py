import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # استخدام أيقونة من النظام بعد التثبيت
    app.setWindowIcon(QIcon("/usr/share/pixmaps/hel-sec-audit.png"))

    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
