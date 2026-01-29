import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QFrame
)
from PyQt5.QtCore import Qt
from api.client import signup_user

class SignupPage(QWidget):
    def __init__(self, app=None):
        super().__init__()
        self.app = app
        self.setWindowTitle("Create Account")
        self.resize(420, 520)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
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
            QPushButton:focus {
                outline: none;
            }
        """)

        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        root.addStretch()

        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(360)

        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(14)
        card_layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Create an Account")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)

        self.alert = QLabel("")
        self.alert.hide()

        card_layout.addWidget(title)
        card_layout.addWidget(self.alert)

        self.username = self.create_input("Username", "Enter your username")
        self.email = self.create_input("Email", "Enter your email")
        self.password = self.create_input("Password", "Enter your password", password=True)
        self.confirm = self.create_input("Confirm Password", "Re-enter your password", password=True)

        card_layout.addWidget(self.username["container"])
        card_layout.addWidget(self.email["container"])
        card_layout.addWidget(self.password["container"])
        card_layout.addWidget(self.confirm["container"])

        self.signup_btn = QPushButton("Sign Up")
        self.signup_btn.clicked.connect(self.handle_signup)

        card_layout.addWidget(self.signup_btn)

        self.login_btn = QPushButton("Already have an account? Log In")
        self.login_btn.setStyleSheet("font-size: 14px; color: #2563eb; background: transparent; border: none;")
        self.login_btn.setFlat(True)
        self.login_btn.clicked.connect(self.app.show_login)
        card_layout.addWidget(self.login_btn)
        root.addWidget(card, alignment=Qt.AlignHCenter)

        root.addStretch()

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

    def show_success(self, msg):
        self.alert.setObjectName("success")
        self.alert.setText(msg)
        self.alert.show()

    def handle_signup(self):
        
        self.signup_btn.setText("Signing up...")
        self.signup_btn.setEnabled(False)
        
        u = self.username["input"].text().strip()
        e = self.email["input"].text().strip()
        p = self.password["input"].text()
        c = self.confirm["input"].text()

        self.alert.hide()

        if not all([u, e, p, c]):
            self.show_error("All fields are required")
            self.signup_btn.setText("Sign Up")
            self.signup_btn.setEnabled(True)
            return

        if p != c:
            self.show_error("Passwords do not match")
            self.signup_btn.setText("Sign Up")
            self.signup_btn.setEnabled(True)
            return

        try:
            res = signup_user(u, e, p , c)
            if res["success"]:
                self.show_success("Signup successful!")
                if self.app and hasattr(self.app, "show_login"):
                    self.app.show_login()
            else:
                self.show_error(res.get("error", "Signup failed. Try again."))
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