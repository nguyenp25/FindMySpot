from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton

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

        self.login_status_label = QLabel('', self)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)
        layout.addWidget(self.login_status_label)

        self.setLayout(layout)
        self.setWindowTitle('FindMySpot - Login')

        self.login_button.clicked.connect(self.login)
        self.register_button.clicked.connect(self.register)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        if self.db.validate_login(username, password):
            self.login_status_label.setText('')
            self.stacked_widget.setCurrentIndex(1)
            
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

        if not username or not password:
            self.login_status_label.setText("Username and password cannot be empty")
            return

        if self.db.user_exists(username):
            self.login_status_label.setText("Username already exists")
            return

        self.db.add_user(username, password)
        self.login_status_label.setText("Registration successful")
        
        if self.db.add_user(username, password):
            self.login_status_label.setText("Registration successful")
            self.clearInputs()
        
    def clearInputs(self):
        self.username_input.setText('')
        self.password_input.setText('')