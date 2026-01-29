from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QApplication
)
from PyQt5.QtCore import Qt, QTimer
from api.client import mockLogin


class LoginPage(QWidget):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.setWindowTitle("Login")
        self.resize(420, 560)
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("""
            QWidget {
                font-family: Arial;
            }

            QFrame#Card {
                background-color: white;
                border: 1px solid #e5e7eb;
                border-radius: 14px;
            }

            QLabel#AppIcon {
                color: #2563eb;
                font-size: 48px;
                font-weight: bold;
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
            
            QPushButton:focus {
                outline: none;
            }
            
            QPushButton:flat {
                font-size: 14px;
                color: #2563eb;
                background: transparent;
                border: none;
            }
            QPushButton:flat:hover {
                text-decoration: underline;
            }
        """)

        # Root layout (full window)
        root = QVBoxLayout(self)
        root.setContentsMargins(0, 0, 0, 0)

        root.addStretch()

        # Header
        header = QVBoxLayout()
        header.setAlignment(Qt.AlignCenter)

        icon = QLabel("⚗")
        icon.setObjectName("AppIcon")
        icon.setAlignment(Qt.AlignCenter)

        title = QLabel("Chemical Equipment Visualizer")
        title.setObjectName("Title")
        title.setAlignment(Qt.AlignCenter)

        subtitle = QLabel("Parameter Analysis Dashboard")
        subtitle.setObjectName("Subtitle")
        subtitle.setAlignment(Qt.AlignCenter)

        header.addWidget(icon)
        header.addSpacing(8)
        header.addWidget(title)
        header.addWidget(subtitle)

        root.addLayout(header)
        root.addSpacing(24)

        card = QFrame()
        card.setObjectName("Card")
        card.setFixedWidth(360)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(24, 24, 24, 24)
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

        self.signup_btn = QPushButton("Don’t have an account? Sign Up")
        self.signup_btn.setFlat(True)
        self.signup_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px;
                color: #2563eb;
                background: transparent;
                border: none;
            }
            QPushButton:hover {
                text-decoration: underline;
            }
        """)
        self.signup_btn.clicked.connect(self.signup)
        layout.addWidget(self.signup_btn)

        root.addWidget(card, alignment=Qt.AlignHCenter)
        root.addStretch()

    def create_input(self, label_text, placeholder, password=False):
        container = QWidget()
        v = QVBoxLayout(container)
        v.setSpacing(4)
        v.setContentsMargins(0, 0, 0, 0)

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

    def signup(self):
        self.app.show_signup()

    def login(self):
        u = self.username["input"].text().strip()
        p = self.password["input"].text().strip()

        self.alert.hide()

        if not u or not p:
            self.show_error("Please enter both username and password")
            return

        self.login_btn.setText("Signing in...")
        self.login_btn.setEnabled(False)

        def handle_login():
            try:
                response = mockLogin(u, p)
                if response.get("success"):
                    self.app.show_dashboard(username=u)
                else:
                    self.show_error(response.get("error", "Login failed."))
            except Exception as e:
                print(e)
                self.show_error("Server not reachable. Please try again. {e}".format(e=str(e)))
            finally:
                self.login_btn.setText("Sign In")
                self.login_btn.setEnabled(True)

        QTimer.singleShot(150, handle_login)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    win = LoginPage(app=app)
    win.show()
    sys.exit(app.exec_())
