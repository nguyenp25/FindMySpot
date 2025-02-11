import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QStackedWidget, QHBoxLayout
from PyQt5.QtCore import Qt

from database import Database
from settingsScreen import SettingsScreen

class LoginScreen(QWidget):
    def __init__(self, stacked_widget, db):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db = db
        self.initUI()

    def initUI(self):
        self.username_label = QLabel('Username', self)
        self.username_input = QLineEdit(self)
        self.password_label = QLabel('Password', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.login_button = QPushButton('Login', self)
        self.register_button = QPushButton('Register', self)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        self.setLayout(layout)
        self.setWindowTitle('FindMySpot - Login')

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.db.validate_login(username, password):
            print("Login successful")
            self.stacked_widget.setCurrentIndex(1)  # Proceed to dashboard
        else:
            print("Invalid username or password")

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if username and password:
            self.db.add_user(username, password)
            print("Registration successful")
        else:
            print("Username and password cannot be empty")

class DashboardScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.header_label = QLabel('Find My Spot\nParking made easy', self)
        self.header_label.setAlignment(Qt.AlignCenter)

        self.map_placeholder = QLabel('Picture of a Map', self)
        self.map_placeholder.setAlignment(Qt.AlignCenter)
        self.map_placeholder.setStyleSheet("background-color: grey; height: 200px;")

        self.find_lot_button = QPushButton('Find a Lot', self)
        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.gotoSettings)

        layout = QVBoxLayout()
        layout.addWidget(self.header_label)
        layout.addWidget(self.map_placeholder)

        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.find_lot_button)
        buttons_layout.addWidget(self.settings_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)
        self.setWindowTitle('Dashboard')

    def gotoSettings(self):
        self.stacked_widget.setCurrentIndex(2)  # Proceed to settings

class MainApp(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.stacked_widget = QStackedWidget()

        self.db = Database()
        self.login_screen = LoginScreen(self.stacked_widget, self.db)
        self.dashboard_screen = DashboardScreen(self.stacked_widget)
        self.settings_screen = SettingsScreen(self.stacked_widget, 1)  # Pass the stacked_widget and dashboard index

        self.stacked_widget.addWidget(self.login_screen)
        self.stacked_widget.addWidget(self.dashboard_screen)
        self.stacked_widget.addWidget(self.settings_screen)

        self.stacked_widget.show()

# Entry point of the application
if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())