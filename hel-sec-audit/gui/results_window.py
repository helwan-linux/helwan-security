# gui/results_window.py
# Displays the security scan results in a user-friendly format.

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QPushButton, QScrollArea, QWidget, QFrame, QSizePolicy, QComboBox, QFileDialog # <--- إضافة QFileDialog
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPalette
import os # <--- إضافة os

class ResultsWindow(QDialog):
    def __init__(self, results):
        super().__init__()
        self.setWindowTitle("Scan Results")
        self.setGeometry(100, 100, 800, 600) # زيادة حجم النافذة
        self.results = results
        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(QLabel("<h1>Security Scan Results</h1>"))

        filter_layout = QVBoxLayout()
        filter_label = QLabel("Filter by Severity:")
        self.filter_combo = QComboBox()
        self.filter_combo.addItem("Show All")
        self.filter_combo.addItem("Secure (Low)")
        self.filter_combo.addItem("Medium")
        self.filter_combo.addItem("High")
        self.filter_combo.currentIndexChanged.connect(self.update_results_display)
        
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.filter_combo)
        main_layout.addLayout(filter_layout)

        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.results_container = QWidget()
        self.results_layout = QVBoxLayout(self.results_container)
        self.results_container.setLayout(self.results_layout)
        self.scroll_area.setWidget(self.results_container)
        
        main_layout.addWidget(self.scroll_area)

        # منطقة الأزرار: إضافة زر "Generate Report"
        # Buttons area: Add "Generate Report" button
        button_layout = QVBoxLayout() # استخدمنا QVBoxLayout عشان كل زرار يبقى في سطر لوحده
        
        generate_report_button = QPushButton("Generate Text Report") # <--- الزر الجديد
        generate_report_button.clicked.connect(self._generate_report) # <--- ربط الزر بدالة
        button_layout.addWidget(generate_report_button)

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.accept)
        button_layout.addWidget(close_button)

        main_layout.addLayout(button_layout) # إضافة منطقة الأزرار للـ main_layout


        self.update_results_display()

    def _generate_report(self):
        options = QFileDialog.Options()
        # options |= QFileDialog.DontUseNativeDialog # لبعض الأنظمة ممكن تحتاج دي لو فيه مشاكل
        
        # فتح نافذة حفظ الملف
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Report", "security_scan_report.txt", "Text Files (*.txt);;All Files (*)", options=options)
        
        if file_name: # لو المستخدم اختار اسم ملف
            try:
                with open(file_name, "w", encoding="utf-8") as f:
                    f.write("Security Scan Report\n")
                    f.write("====================\n\n")
                    
                    # يمكنك إضافة تاريخ ووقت الفحص هنا
                    # import datetime
                    # f.write(f"Scan Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")

                    for i, result in enumerate(self.results):
                        f.write(f"--- Check #{i+1}: {result['check_name']} ---\n")
                        f.write(f"Status: {'SECURE' if result['is_secure'] else 'VULNERABLE'}\n")
                        f.write(f"Title: {result['title']}\n")
                        f.write(f"Severity: {result['severity']}\n")
                        f.write(f"Description: {result['description']}\n")
                        if result["solution"] and result["solution"] != "N/A":
                            f.write(f"Solution: {result['solution']}\n")
                        f.write("\n") # سطر فارغ بين كل فحص والتاني
                
                # ممكن تظهر رسالة للمستخدم إن التقرير اتحفظ بنجاح
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.information(self, "Report Saved", f"Report saved successfully to:\n{file_name}")

            except Exception as e:
                from PyQt5.QtWidgets import QMessageBox
                QMessageBox.critical(self, "Error Saving Report", f"Could not save report:\n{e}")


    def update_results_display(self):
        for i in reversed(range(self.results_layout.count())):
            widget = self.results_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        selected_filter = self.filter_combo.currentText()

        for result in self.results:
            if selected_filter == "Show All":
                pass
            elif selected_filter == "Secure (Low)" and (result["severity"] != "Low" or not result["is_secure"]):
                continue
            elif selected_filter == "Medium" and result["severity"] != "Medium":
                continue
            elif selected_filter == "High" and result["severity"] != "High":
                continue
            
            result_frame = QFrame()
            result_frame.setFrameShape(QFrame.StyledPanel)
            result_frame.setFrameShadow(QFrame.Raised)
            result_frame_layout = QVBoxLayout()
            result_frame.setLayout(result_frame_layout)

            background_color = QColor("white")
            if result["is_secure"]:
                background_color = QColor("#e6ffe6")
            else:
                if result["severity"] == "High":
                    background_color = QColor("#ffe6e6")
                elif result["severity"] == "Medium":
                    background_color = QColor("#fff2e6")
                else: 
                    background_color = QColor("#f0f0f0")

            palette = result_frame.palette()
            palette.setColor(QPalette.Background, background_color)
            result_frame.setPalette(palette)
            result_frame.setAutoFillBackground(True)

            status_text = "SECURE" if result["is_secure"] else "VULNERABLE"
            
            result_frame_layout.addWidget(QLabel(f"<h2>{result['check_name']} - Status: {status_text}</h2>"))
            result_frame_layout.addWidget(QLabel(f"<b>Title:</b> {result['title']}"))
            result_frame_layout.addWidget(QLabel(f"<b>Severity:</b> <span style='color:{self._get_severity_color(result['severity'])}'>{result['severity']}</span>"))
            result_frame_layout.addWidget(QLabel(f"<b>Description:</b> {result['description']}"))
            
            if result["solution"] and result["solution"] != "N/A":
                solution_label = QLabel(f"<b>Solution:</b> {result['solution']}")
                solution_label.setWordWrap(True)
                result_frame_layout.addWidget(solution_label)

            result_frame_layout.addSpacing(10) 

            self.results_layout.addWidget(result_frame)
        
        self.results_layout.addStretch(1)

    def _get_severity_color(self, severity):
        if severity == "High":
            return "red"
        elif severity == "Medium":
            return "orange"
        elif severity == "Low":
            return "green"
        else:
            return "black"
