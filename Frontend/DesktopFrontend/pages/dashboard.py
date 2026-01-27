from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt

from components.navbar import Navbar
from components.file_upload import FileUpload
from components.summary_cards import SummaryCards
from components.charts import Charts
from components.data_table import DataTable
from components.history_list import HistoryList


class DashboardPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setObjectName("Dashboard")
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget#Dashboard {
                background-color: #f8fafc; /* slate-50 */
            }

            QFrame#Container {
                background: transparent;
            }

            QFrame#Card {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)
        root.setSpacing(0)

        self.navbar = Navbar("Guest", self.logout)
        root.addWidget(self.navbar)

        container = QFrame()
        container.setObjectName("Container")
        container_layout = QHBoxLayout(container)
        container_layout.setContentsMargins(24, 32, 24, 32)
        container_layout.setSpacing(24)

        sidebar = QVBoxLayout()
        sidebar.setSpacing(24)
        sidebar.setAlignment(Qt.AlignTop)

        self.upload = FileUpload(self.on_upload)
        self.history = HistoryList(self.on_select)

        self.wrap_card(self.upload, sidebar)
        self.wrap_card(self.history, sidebar)

        main = QVBoxLayout()
        main.setSpacing(24)
        main.setAlignment(Qt.AlignTop)

        self.summary = SummaryCards()
        self.charts = Charts()
        self.table = DataTable()

        self.wrap_card(self.summary, main)
        self.wrap_card(self.charts, main)
        self.wrap_card(self.table, main)

        container_layout.addLayout(sidebar, 1)
        container_layout.addLayout(main, 3)

        wrapper = QHBoxLayout()
        wrapper.addStretch()
        wrapper.addWidget(container)
        wrapper.addStretch()

        root.addLayout(wrapper)

    def wrap_card(self, widget, layout):
        """Wrap components in card-style containers"""
        card = QFrame()
        card.setObjectName("Card")

        v = QVBoxLayout(card)
        v.setContentsMargins(16, 16, 16, 16)
        v.addWidget(widget)

        layout.addWidget(card)

    def on_upload(self, filename):
        dataset = filename
        self.summary.update(dataset)
        self.charts.update(dataset)
        self.table.update(dataset)

    def on_select(self, dataset):
        self.summary.update(dataset)
        self.charts.update(dataset)
        self.table.update(dataset)

    def logout(self):
        self.app.show_login()
