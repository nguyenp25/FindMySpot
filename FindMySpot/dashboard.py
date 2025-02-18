import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

class DashboardScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        self.dashboard_label = QLabel('Dashboard - Main app functionality', self)
        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.gotoSettings)

        layout = QVBoxLayout()
        layout.addWidget(self.dashboard_label)
        layout.addWidget(self.settings_button)

        self.setLayout(layout)
        self.setWindowTitle('Dashboard')

    def gotoSettings(self):
        self.stacked_widget.setCurrentIndex(2)