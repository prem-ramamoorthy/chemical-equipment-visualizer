from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class HistoryList(QWidget):
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
        card_layout.setSpacing(14)

        header = QLabel("Upload History")
        header.setFont(QFont("Inter", 11, QFont.Bold))
        header.setStyleSheet("color: #0f172a;")

        card_layout.addWidget(header)

        self.list_widget = QListWidget()
        self.list_widget.setSpacing(6)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        self.list_widget.setStyleSheet("""
            QListWidget {
                border: none;
                outline: none;
            }
            QListWidget::item {
                background: #f8fafc;
                border-radius: 8px;
                padding: 10px;
            }
            QListWidget::item:hover {
                background: #f1f5f9;
            }
            QListWidget::item:selected {
                background: #eff6ff;
                border: 1px solid #93c5fd;
            }
        """)

        for i in range(5):
            item = QListWidgetItem()
            item.setText(f"dataset_{i}.csv\nToday • {10 + i} items")
            item.setTextAlignment(Qt.AlignVCenter)
            item.setFont(QFont("Inter", 9))
            self.list_widget.addItem(item)

        card_layout.addWidget(self.list_widget)
        outer_layout.addWidget(card)
