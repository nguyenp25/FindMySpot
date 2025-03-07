from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

class DashboardScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.dashboard_label = QLabel('Dashboard - Main app functionality', self)
        self.settings_button = QPushButton('Settings', self)
        self.logout_button = QPushButton('Logout', self)  # Add a logout button

        self.settings_button.clicked.connect(self.gotoSettings)
        self.logout_button.clicked.connect(self.logout)  # Connect to logout function

        layout = QVBoxLayout()
        layout.addWidget(self.dashboard_label)
        layout.addWidget(self.settings_button)
        layout.addWidget(self.logout_button)  # Add the button to the layout

        self.setLayout(layout)
        self.setWindowTitle('Dashboard')

    def gotoSettings(self):
        self.stacked_widget.setCurrentIndex(2)

    def logout(self):
        self.stacked_widget.setCurrentIndex(0)  # Go back to the Login screen