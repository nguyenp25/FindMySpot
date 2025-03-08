from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit, QMessageBox

class UserManagementScreen(QWidget):
    def __init__(self, stacked_widget, db):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db = db
        self.username = None
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        label = QLabel("User Management Screen")
        layout.addWidget(label)

        # Add new widgets for changing username and password
        self.username_label = QLabel('New Username:', self)
        self.username_input = QLineEdit(self)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)

        self.password_label = QLabel('New Password:', self)
        self.password_input = QLineEdit(self)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.change_button = QPushButton('Change Username/Password', self)
        self.change_button.clicked.connect(self.changeUsernamePassword)
        layout.addWidget(self.change_button)

        self.back_button = QPushButton('Back to Settings', self)
        self.back_button.clicked.connect(self.gotoSettingsScreen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

    def set_current_user(self, username):
        self.current_user = username

    def changeUsernamePassword(self):
        new_username = self.username_input.text()
        new_password = self.password_input.text()

        if new_username and new_password:
            success = self.db.change_username_password(self.db.get_user(self.current_user)['username'], new_username, new_password)

            if success:
                QMessageBox.information(self, 'Success', 'Username and Password changed successfully.')
            else:
                QMessageBox.warning(self, 'Error', 'Failed to change Username and Password.')
        else:
            QMessageBox.warning(self, 'Error', 'Please enter both new Username and Password.')

    def gotoSettingsScreen(self):
        from settings_screen import SettingsScreen

        for index in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(index)
            if isinstance(widget, SettingsScreen):
                self.stacked_widget.setCurrentIndex(index)
                break
