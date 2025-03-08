from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton
from twilio.rest import Client

class LoginScreen(QWidget):
    def __init__(self, stacked_widget, db, widget_indices):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.db = db
        self.widget_indices = widget_indices
        self.initUI()


    def initUI(self):
        self.username_label = QLabel('Username', self)
        self.username_input = QLineEdit(self)
        self.password_label = QLabel('Password', self)
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.phone_number_label = QLabel('Phone Number', self)
        self.phone_number_input = QLineEdit(self)
        self.login_button = QPushButton('Login', self)
        self.register_button = QPushButton('Register', self)
        self.login_status_label = QLabel('', self)
        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.login_status_label)
        layout.addWidget(self.phone_number_label)
        layout.addWidget(self.phone_number_input)
        self.setLayout(layout)
        self.setWindowTitle('FindMySpot - Login')
        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)
    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.db.validate_login(username, password):
            self.login_status_label.setText('')

            payment_screen = self.stacked_widget.widget(5)
            payment_screen.set_current_user(username)

            user_screen = self.stacked_widget.widget(3)
            user_screen.set_current_user(username)

            main_window = self.stacked_widget.widget(6)  # Assuming MainWindow is at index 1
            main_window.set_current_user(username)  # Set the current user in MainWindow

            dashboard_screen = self.stacked_widget.widget(1)
            dashboard_screen.set_current_user(username)
            dashboard_screen.update_dashboard()

            self.stacked_widget.setCurrentIndex(1)
            self.clearInputs()
            
        else:
            self.login_status_label.setText('Invalid username or password')
        if self.db.validate_login(username, password):
            self.login_status_label.setText('')
            self.stacked_widget.setCurrentIndex(1)
            self.clearInputs()
        else:
            self.login_status_label.setText('Invalid username or password')

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        phone = self.phone_number_input.text()  # Get the phone number from input

        if not username or not password or not phone:
            self.login_status_label.setText("Username, password, or phone cannot be empty")
            return

        if len(password) < 4:
            self.login_status_label.setText("Password must be at least 4 characters long")
            return

        if self.db.user_exists(username):
            self.login_status_label.setText("Username already exists")
            return

        if self.db.add_user(username, password, phone):
            self.login_status_label.setText("Registration successful")
            self.send_sms_notification(phone)  # Send SMS notification
            self.clearInputs()

    def send_sms_notification(self, user_phone):
        account_sid = 'AC2ea1c971ea162d98295bf49cbb1a984f'
        auth_token = 'a1284fed6431c233d1c0b59849dad731'
        client = Client(account_sid, auth_token)
        twilio_number = '+18667262459'  # Ensure the number is in E.164 format
        message_body = 'Welcome! Thank you for registering with FindMySpot.'
        try:
            message = client.messages.create(
                body=message_body,
                from_=twilio_number,
                to=user_phone
            )
            print(f"Message sent: {message.sid}")
        except Exception as e:
            print(f"Failed to send SMS: {e}")
    def clearInputs(self):
        self.username_input.clear()
        self.password_input.clear()
        self.phone_number_input.clear()
# The following should be outside of the class definition
# and typically included only if this script is the main entry point for the application.
if __name__ == '__main__':
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    # Replace None with actual instances if necessary
    login_screen = LoginScreen(None, None)  # Replace with the actual stacked_widget and db
    login_screen.show()
    app.exec_()