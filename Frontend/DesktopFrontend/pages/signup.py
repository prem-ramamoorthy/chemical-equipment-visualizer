import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QHBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from api.client import signup_user


class SignupPage(QWidget):
    def __init__(self , parent = 0):
        super().__init__()
        self.setWindowTitle("Create Account")
        self.setFixedSize(420, 520)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #f9fafb;
                font-family: Arial;
            }
            QFrame#Card {
                background-color: white;
                border-radius: 14px;
            }
            QLabel#Title {
                font-size: 22px;
                font-weight: 700;
                color: #1f2937;
            }
            QLabel.label {
                font-size: 12px;
                font-weight: 600;
                color: #374151;
            }
            QLineEdit {
                padding: 10px 12px;
                border: 1px solid #d1d5db;
                border-radius: 8px;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 2px solid #3b82f6;
            }
            QPushButton {
                background-color: #2563eb;
                color: white;
                font-size: 15px;
                font-weight: 600;
                padding: 12px;
                border-radius: 10px;
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
            QLabel#success {
                background-color: #dcfce7;
                color: #15803d;
                padding: 8px;
                border-radius: 8px;
                font-size: 13px;
            }
        """)

        root = QVBoxLayout(self)
        root.setAlignment(Qt.AlignCenter)

        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(360)

        layout = QVBoxLayout(card)
        layout.setSpacing(14)

        title = QLabel("Create an Account")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)

        self.alert = QLabel("")
        self.alert.hide()

        layout.addWidget(title)
        layout.addWidget(self.alert)

        self.username = self.create_input("Username")
        self.email = self.create_input("Email")
        self.password = self.create_input("Password", password=True)
        self.confirm = self.create_input("Confirm Password", password=True)

        layout.addWidget(self.username["container"])
        layout.addWidget(self.email["container"])
        layout.addWidget(self.password["container"])
        layout.addWidget(self.confirm["container"])

        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.clicked.connect(self.handle_signup)

        layout.addWidget(self.signup_btn)

        footer = QLabel(
            'Already have an account? <a href="#">Log In</a>'
        )
        footer.setAlignment(Qt.AlignCenter)
        footer.setStyleSheet("""
            QLabel {
                font-size: 12px;
                color: #6b7280;
            }
            a {
                color: #2563eb;
                text-decoration: none;
                font-weight: 600;
            }
        """)

        layout.addWidget(footer)
        root.addWidget(card)

    def create_input(self, label_text, password=False):
        container = QWidget()
        v = QVBoxLayout(container)
        v.setSpacing(4)

        label = QLabel(label_text)
        label.setProperty("class", "label")

        inp = QLineEdit()
        if password:
            inp.setEchoMode(QLineEdit.Password)

        v.addWidget(label)
        v.addWidget(inp)

        return {"container": container, "input": inp}

    def show_error(self, msg):
        self.alert.setObjectName("error")
        self.alert.setText(msg)
        self.alert.show()

    def show_success(self, msg):
        self.alert.setObjectName("success")
        self.alert.setText(msg)
        self.alert.show()

    def handle_signup(self):
        u = self.username["input"].text().strip()
        e = self.email["input"].text().strip()
        p = self.password["input"].text()
        c = self.confirm["input"].text()

        self.alert.hide()

        if not all([u, e, p, c]):
            self.show_error("All fields are required")
            return

        if p != c:
            self.show_error("Passwords do not match")
            return

        self.signup_btn.setText("Signing up...")
        self.signup_btn.setEnabled(False)

        try:
            res = signup_user(u, e, p)
            if res.status_code == 201:
                self.show_success("Signup successful!")
            else:
                self.show_error("Signup failed. Try again.")
        except Exception:
            self.show_error("Server not reachable")
        finally:
            self.signup_btn.setText("Sign Up")
            self.signup_btn.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = SignupPage()
    win.show()
    sys.exit(app.exec_())
