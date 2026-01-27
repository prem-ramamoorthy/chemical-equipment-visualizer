from PyQt5.QtWidgets import (
    QFrame, QWidget, QLabel,
    QVBoxLayout, QHBoxLayout
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class SummaryCard(QFrame):
    def __init__(self, label, value, unit="", icon="■", icon_bg="#dbeafe", icon_color="#2563eb"):
        super().__init__()

        self.setStyleSheet("""
            QFrame {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 14px;
            }
            QFrame:hover {
                border-color: #cbd5f5;
            }
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        left = QVBoxLayout()
        left.setSpacing(6)

        label_widget = QLabel(label)
        label_widget.setFont(QFont("Inter", 9))
        label_widget.setStyleSheet("color: #64748b;")

        value_row = QHBoxLayout()
        value_row.setSpacing(4)

        value_widget = QLabel(str(value))
        value_widget.setFont(QFont("Inter", 16, QFont.Bold))
        value_widget.setStyleSheet("color: #0f172a;")

        unit_widget = QLabel(unit)
        unit_widget.setFont(QFont("Inter", 9))
        unit_widget.setStyleSheet("color: #64748b;")

        value_row.addWidget(value_widget)
        if unit:
            value_row.addWidget(unit_widget)
        value_row.addStretch()

        left.addWidget(label_widget)
        left.addLayout(value_row)

        icon_widget = QLabel(icon)
        icon_widget.setAlignment(Qt.AlignCenter)
        icon_widget.setFixedSize(40, 40)
        icon_widget.setStyleSheet(f"""
            background: {icon_bg};
            color: {icon_color};
            border-radius: 10px;
            font-size: 18px;
            font-weight: bold;
        """)

        layout.addLayout(left)
        layout.addStretch()
        layout.addWidget(icon_widget)


class SummaryCards(QWidget):
    def __init__(self, summary=None):
        super().__init__()

        layout = QHBoxLayout(self)
        layout.setSpacing(16)

        if summary is None:
            for _ in range(4):
                skeleton = QFrame()
                skeleton.setFixedHeight(96)
                skeleton.setStyleSheet("""
                    QFrame {
                        background: #f1f5f9;
                        border-radius: 14px;
                        border: 1px solid #e2e8f0;
                    }
                """)
                layout.addWidget(skeleton)
            return

        layout.addWidget(
            SummaryCard(
                "Total Equipment",
                summary["total_count"],
                icon="▣",
                icon_bg="#dbeafe",
                icon_color="#2563eb"
            )
        )

        layout.addWidget(
            SummaryCard(
                "Avg Flowrate",
                summary["avg_flowrate"],
                "m³/h",
                icon="💧",
                icon_bg="#cffafe",
                icon_color="#0891b2"
            )
        )

        layout.addWidget(
            SummaryCard(
                "Avg Pressure",
                summary["avg_pressure"],
                "bar",
                icon="⏱",
                icon_bg="#ffedd5",
                icon_color="#ea580c"
            )
        )

        layout.addWidget(
            SummaryCard(
                "Avg Temperature",
                summary["avg_temperature"],
                "°C",
                icon="🌡",
                icon_bg="#fee2e2",
                icon_color="#dc2626"
            )
        )
