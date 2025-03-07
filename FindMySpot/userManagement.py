from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

class UserManagementScreen(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()

    def initUI(self):
        label = QLabel("User Management Settings", self)
        layout = QVBoxLayout()
        layout.addWidget(label)

        # Back to Settings button
        self.back_button = QPushButton('Back to Settings', self)
        self.back_button.clicked.connect(self.gotoSettings)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def gotoSettings(self):
        # Assuming the SettingsScreen is at a specific index
        # Replace 0 with the actual index of SettingsScreen in your stacked_widget
        self.stacked_widget.setCurrentIndex(0)