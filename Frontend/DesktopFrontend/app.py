from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout
from pages.login import LoginPage
from pages.signup import SignupPage
from pages.dashboard import DashboardPage

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.resize(1200, 800)

        self.stack = QStackedWidget()

        self.login = LoginPage(self)
        self.signup = SignupPage(self)
        self.dashboard = DashboardPage(self)

        self.stack.addWidget(self.login)
        self.stack.addWidget(self.signup)
        self.stack.addWidget(self.dashboard)

        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        self.show_login()

    def show_login(self):
        self.stack.setCurrentWidget(self.login)

    def show_signup(self):
        self.stack.setCurrentWidget(self.signup)

    def show_dashboard(self , username=None):
        self.dashboard = DashboardPage(self, username=username)
        self.stack.addWidget(self.dashboard)
        self.stack.setCurrentWidget(self.dashboard)