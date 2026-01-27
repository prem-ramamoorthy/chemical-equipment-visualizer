from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QHeaderView, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont


class DataTable(QWidget):
    HEADERS = [
        ("name", "Equipment Name"),
        ("type", "Type"),
        ("flowrate", "Flowrate (m³/h)"),
        ("pressure", "Pressure (bar)"),
        ("temperature", "Temp (°C)"),
    ]

    def __init__(self):
        super().__init__()
        self.sort_column = -1
        self.sort_order = Qt.AscendingOrder
        self.data = []

        self.init_ui()

    # ---------------- UI ----------------
    def init_ui(self):
        self.setStyleSheet("""
            QFrame#Card {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 12px;
            }

            QTableWidget {
                border: none;
                gridline-color: #e5e7eb;
                font-size: 13px;
            }

            QHeaderView::section {
                background: #f1f5f9;
                padding: 12px;
                border: none;
                font-size: 11px;
                font-weight: 600;
                text-transform: uppercase;
                color: #64748b;
            }

            QTableWidget::item {
                padding: 10px;
            }

            QTableWidget::item:selected {
                background: #e0f2fe;
            }

            QTableWidget::item:hover {
                background: #f8fafc;
            }
        """)

        root = QVBoxLayout(self)

        self.card = QFrame()
        self.card.setObjectName("Card")
        card_layout = QVBoxLayout(self.card)
        card_layout.setContentsMargins(0, 0, 0, 0)

        # ---------- Header ----------
        header = QHBoxLayout()
        header.setContentsMargins(16, 12, 16, 12)

        title = QLabel("📋  Equipment Data")
        title.setFont(QFont("", 14, QFont.Bold))

        self.count_badge = QLabel("")
        self.count_badge.setStyleSheet("""
            background: #dbeafe;
            color: #1d4ed8;
            border-radius: 10px;
            padding: 2px 8px;
            font-size: 11px;
            font-weight: 600;
        """)

        header.addWidget(title)
        header.addWidget(self.count_badge)
        header.addStretch()

        # ---------- Table ----------
        self.table = QTableWidget(0, len(self.HEADERS))
        self.table.setHorizontalHeaderLabels([h[1] for h in self.HEADERS])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSortingEnabled(False)
        self.table.horizontalHeader().sectionClicked.connect(self.handle_sort)

        card_layout.addLayout(header)
        card_layout.addWidget(self.table)

        root.addWidget(self.card)

        self.render_empty_state()

    # ---------------- Empty State ----------------
    def render_empty_state(self):
        self.table.setRowCount(1)
        self.table.setSpan(0, 0, 1, self.table.columnCount())

        item = QTableWidgetItem(
            "No data available. Upload a dataset to view equipment details."
        )
        item.setTextAlignment(Qt.AlignCenter)
        item.setForeground(QColor("#64748b"))
        self.table.setItem(0, 0, item)

        self.count_badge.setText("0 items")

    # ---------------- Update Data ----------------
    def update_data(self, data):
        """
        data: list of dicts
        """
        self.data = data

        if not data:
            self.render_empty_state()
            return

        self.count_badge.setText(f"{len(data)} items")
        self.table.setRowCount(len(data))
        self.table.setSpan(0, 0, 1, 1)

        for row, item in enumerate(data):
            self.add_row(row, item)

    # ---------------- Row Rendering ----------------
    def add_row(self, row, item):
        for col, (key, _) in enumerate(self.HEADERS):
            value = item[key]

            cell = QTableWidgetItem()

            if isinstance(value, float):
                cell.setText(f"{value:.1f}")
                cell.setFont(QFont("Monospace"))
                cell.setForeground(QColor("#475569"))
            else:
                cell.setText(str(value))

            if key == "type":
                cell.setTextAlignment(Qt.AlignCenter)
                cell.setForeground(self.type_color(value))
                cell.setBackground(self.type_bg(value))

            self.table.setItem(row, col, cell)

    # ---------------- Sorting ----------------
    def handle_sort(self, column):
        if self.sort_column == column:
            if self.sort_order == Qt.AscendingOrder:
                self.sort_order = Qt.DescendingOrder
            else:
                self.sort_column = -1
                self.sort_order = Qt.AscendingOrder
                self.update_data(self.data)
                return
        else:
            self.sort_column = column
            self.sort_order = Qt.AscendingOrder

        key = self.HEADERS[column][0]

        self.data.sort(
            key=lambda x: x[key],
            reverse=self.sort_order == Qt.DescendingOrder
        )

        self.update_data(self.data)

    # ---------------- Type Badges ----------------
    def type_color(self, t):
        return {
            "Pump": QColor("#1d4ed8"),
            "Reactor": QColor("#0f766e"),
            "Heat Exchanger": QColor("#c2410c"),
        }.get(t, QColor("#334155"))

    def type_bg(self, t):
        return {
            "Pump": QColor("#dbeafe"),
            "Reactor": QColor("#ccfbf1"),
            "Heat Exchanger": QColor("#ffedd5"),
        }.get(t, QColor("#f1f5f9"))
