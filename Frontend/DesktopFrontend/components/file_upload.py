from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QFileDialog, QFrame
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class FileUpload(QWidget):
    fileSelected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__()

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        card = QFrame()
        card.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
            }
        """)

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(20, 20, 20, 20)
        card_layout.setSpacing(16)

        title = QLabel("Upload Dataset")
        title.setFont(QFont("Inter", 11, QFont.Bold))
        title.setStyleSheet("color: #0f172a;")

        card_layout.addWidget(title)

        self.drop_area = QFrame()
        self.drop_area.setMinimumHeight(180)
        self.drop_area.setCursor(Qt.PointingHandCursor)
        self.drop_area.setStyleSheet("""
            QFrame {
                border: 2px dashed #cbd5e1;
                border-radius: 10px;
                background: #f8fafc;
            }
            QFrame:hover {
                border-color: #3b82f6;
                background: #f1f5f9;
            }
        """)

        drop_layout = QVBoxLayout(self.drop_area)
        drop_layout.setAlignment(Qt.AlignCenter)
        drop_layout.setSpacing(8)

        icon = QLabel("⬆")
        icon.setAlignment(Qt.AlignCenter)
        icon.setStyleSheet("font-size: 36px; color: #94a3b8;")

        self.main_text = QLabel("Drop your CSV file here or browse")
        self.main_text.setAlignment(Qt.AlignCenter)
        self.main_text.setStyleSheet("""
            font-size: 13px;
            font-weight: 500;
            color: #0f172a;
        """)

        self.sub_text = QLabel("Supports equipment parameter datasets")
        self.sub_text.setAlignment(Qt.AlignCenter)
        self.sub_text.setStyleSheet("""
            font-size: 11px;
            color: #64748b;
        """)

        drop_layout.addWidget(icon)
        drop_layout.addWidget(self.main_text)
        drop_layout.addWidget(self.sub_text)

        self.drop_area.mousePressEvent = self.open_file_dialog

        card_layout.addWidget(self.drop_area)
        outer_layout.addWidget(card)

    def open_file_dialog(self, event):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv)"
        )

        if file_path:
            filename = file_path.split("/")[-1]
            self.main_text.setText("Dataset uploaded successfully")
            self.main_text.setStyleSheet("""
                font-size: 13px;
                font-weight: 500;
                color: #059669;
            """)
            self.sub_text.setText(filename)
            self.fileSelected.emit(file_path)
