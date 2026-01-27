from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame , QApplication
)
from PyQt5.QtCore import Qt, QTimer
from api.client import mockLogin

class LoginPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.init_ui()

    def center(self):
        qr = self.frameGeometry()
        cp = QApplication.desktop().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
            background-color: #f1f5f9;
            font-family: Arial;
            }

            QFrame#Card {
            border: 1px solid #e5e7eb;
            border-radius: 14px;
            }

            QLabel#AppIcon {
            color: #2563eb;
            font-size: 50px;
            font-weight: bold;
            border-radius: 16px;
            min-width: 64px;
            min-height: 64px;
            }

            QLabel#Title {
            font-size: 22px;
            font-weight: 700;
            color: #0f172a;
            }

            QLabel#Subtitle {
            font-size: 12px;
            color: #475569;
            }

            QLabel#SectionTitle {
            font-size: 18px;
            font-weight: 600;
            color: #0f172a;
            }

            QLabel.label {
            font-size: 12px;
            font-weight: 600;
            color: #334155;
            }

            QLineEdit {
            padding: 10px 12px;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            font-size: 14px;
            }

            QLineEdit:focus {
            border: 2px solid #3b82f6;
            }

            QPushButton {
            background-color: #2563eb;
            color: white;
            padding: 12px;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 600;
            }

            QPushButton:hover {
            background-color: #1d4ed8;
            }

            QPushButton:disabled {
            background-color: #93c5fd;
            }

            QLabel#error {
            background-color: #fee2e2;
            color: #b91c1c;
            padding: 8px;
            border-radius: 8px;
            font-size: 13px;
            }
        """)

        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)

        header = QVBoxLayout()
        header.setAlignment(Qt.AlignCenter)

        icon = QLabel("⚗")
        icon.setObjectName("AppIcon")
        icon.setAlignment(Qt.AlignCenter)

        title = QLabel("Chemical Equipment Visualizer")
        title.setObjectName("Title")

        subtitle = QLabel("Parameter Analysis Dashboard")
        subtitle.setObjectName("Subtitle")

        header.addWidget(icon)
        header.addSpacing(10)
        header.addWidget(title)
        header.addWidget(subtitle)

        root.addLayout(header)
        root.addSpacing(24)

        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(360)

        layout = QVBoxLayout(card)
        layout.setSpacing(14)

        section_title = QLabel("Sign in to continue")
        section_title.setObjectName("SectionTitle")
        section_title.setAlignment(Qt.AlignCenter)

        self.alert = QLabel("")
        self.alert.hide()

        layout.addWidget(section_title)
        layout.addWidget(self.alert)

        self.username = self.create_input("Username", "Enter your username")
        self.password = self.create_input("Password", "Enter your password", password=True)

        layout.addWidget(self.username["container"])
        layout.addWidget(self.password["container"])

        self.login_btn = QPushButton("Sign In")
        self.login_btn.clicked.connect(self.login)

        layout.addWidget(self.login_btn)

        demo = QLabel("Demo mode enabled — any credentials are accepted")
        demo.setAlignment(Qt.AlignCenter)
        demo.setStyleSheet("font-size: 11px; color: #64748b;")

        layout.addWidget(demo)

        root.addWidget(card)

    def create_input(self, label_text, placeholder, password=False):
        container = QWidget()
        v = QVBoxLayout(container)
        v.setSpacing(4)

        label = QLabel(label_text)
        label.setProperty("class", "label")

        inp = QLineEdit()
        inp.setPlaceholderText(placeholder)
        if password:
            inp.setEchoMode(QLineEdit.Password)

        v.addWidget(label)
        v.addWidget(inp)

        return {"container": container, "input": inp}

    def show_error(self, msg):
        self.alert.setObjectName("error")
        self.alert.setText(msg)
        self.alert.show()

    def login(self):
        u = self.username["input"].text().strip()
        p = self.password["input"].text().strip()

        self.alert.hide()

        if not u or not p:
            self.show_error("Please enter both username and password")
            return

        self.login_btn.setText("Signing in...")
        self.login_btn.setEnabled(False)

        try:
            if mockLogin(u, p):
                self.app.show_dashboard()
            else:
                self.show_error("Invalid credentials. Please try again.")
        except Exception:
            self.show_error("An unexpected error occurred. Please try again.")
        finally:
            self.login_btn.setText("Sign In")
            self.login_btn.setEnabled(True)