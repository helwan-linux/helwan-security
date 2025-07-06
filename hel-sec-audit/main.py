import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon

from gui.main_window import MainWindow

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # تعيين أيقونة التطبيق العامة (ستظهر في شريط المهام وعنوان النافذة)
    # تأكد من أن المسار "gui/assets/app_icon.png" صحيح وأن الملف موجود.
    app.setWindowIcon(QIcon("gui/assets/app_icon.png")) 

    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
