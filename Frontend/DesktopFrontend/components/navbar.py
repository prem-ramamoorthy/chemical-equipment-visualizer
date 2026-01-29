from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Navbar(QWidget):
    def __init__(self, username="User", on_logout=None, parent=None):
        super().__init__(parent)

        self.setFixedHeight(64)

        # Outer container
        outer = QVBoxLayout(self)
        outer.setContentsMargins(0, 0, 0, 0)

        nav = QFrame()
        nav.setStyleSheet("""
            QFrame {
                background: white;
                border-bottom: 1px solid #e2e8f0;
            }
        """)

        layout = QHBoxLayout(nav)
        layout.setContentsMargins(24, 0, 24, 0)
        layout.setSpacing(16)

        # ---- Left Section (Icon + Title) ----
        left = QHBoxLayout()
        left.setSpacing(12)

        icon = QLabel("⚗")  # Beaker icon substitute
        icon.setAlignment(Qt.AlignCenter)
        icon.setFixedSize(40, 40)
        icon.setStyleSheet("""
            background: #2563eb;
            color: white;
            border-radius: 8px;
            font-size: 20px;
        """)

        title_box = QVBoxLayout()
        title_box.setSpacing(0)

        title = QLabel("Chemical Equipment Visualizer")
        title.setFont(QFont("Inter", 11, QFont.Bold))
        title.setStyleSheet("color: #0f172a;")

        subtitle = QLabel("Parameter Analysis Dashboard")
        subtitle.setFont(QFont("Inter", 8))
        subtitle.setStyleSheet("color: #64748b;")

        title_box.addWidget(title)
        title_box.addWidget(subtitle)

        left.addWidget(icon)
        left.addLayout(title_box)

        right = QHBoxLayout()
        right.setSpacing(12)

        user_badge = QLabel(f"● {username}")
        user_badge.setStyleSheet("""
            QLabel {
                background: #f1f5f9;
                color: #1e293b;
                padding: 6px 12px;
                border-radius: 999px;
                font-size: 12px;
                font-weight: 500;
            }
        """)

        logout_btn = QPushButton("Logout")
        logout_btn.setCursor(Qt.PointingHandCursor)
        logout_btn.setStyleSheet("""
            QPushButton {
                border: none;
                padding: 8px 14px;
                border-radius: 8px;
                background: transparent;
                color: #475569;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #f1f5f9;
                color: #0f172a;
            }
        """)

        if on_logout:
            logout_btn.clicked.connect(on_logout)

        right.addWidget(user_badge)
        right.addWidget(logout_btn)

        layout.addLayout(left)
        layout.addStretch()
        layout.addLayout(right)

        outer.addWidget(nav)
