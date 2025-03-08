from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QHBoxLayout, QFormLayout

class PaymentInformationScreen(QWidget):
    def __init__(self, stacked_widget, db, main_app):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.initUI()
        self.db = db
        self.current_user = None
        self.main_app = main_app

    def initUI(self):
        layout = QVBoxLayout()

        # Title Label
        title_label = QLabel("Payment Information")
        layout.addWidget(title_label)

        # Form layout for payment details
        form_layout = QFormLayout()

        # In PaymentInformationScreen class of payment_information_screen.py

        # Add UI elements for credit card input and top-up amount
        self.card_number_input = QLineEdit(self)
        self.top_up_amount_input = QLineEdit(self)
        self.top_up_button = QPushButton('Top Up', self)
        self.top_up_button.clicked.connect(self.top_up_balance)

        layout.addWidget(QLabel('Card Number:'))
        layout.addWidget(self.card_number_input)
        layout.addWidget(QLabel('Top-Up Amount:'))
        layout.addWidget(self.top_up_amount_input)
        layout.addWidget(self.top_up_button)


        # Back to Settings Button
        self.back_button = QPushButton('Back to Settings', self)
        self.back_button.clicked.connect(self.gotoSettingsScreen)
        layout.addWidget(self.back_button)

        self.setLayout(layout)


    def top_up_balance(self):
        card_number = self.card_number_input.text().replace(" ", "")  # Remove spaces if any
        top_up_amount = self.top_up_amount_input.text()

        # Validate credit card number length
        if len(card_number) != 16 or not card_number.isdigit():
            # Show an error message or handle the error appropriately
            print("Invalid card number. Please enter a 16-digit credit card number.")
            return

        try:
            top_up_amount = float(top_up_amount)
        except ValueError:
            # Handle invalid top-up amount (not a number)
            print("Invalid top-up amount. Please enter a valid number.")
            return

        # Proceed with the top-up if the card number is valid
        dashboard_index = self.main_app.widget_indices.get('dashboard_screen')
        dashboard_screen = self.stacked_widget.widget(dashboard_index)

        # Update the balance in the database
        self.db.update_account_balance(self.current_user, top_up_amount)

        # Clear the inputs and update the dashboard
        self.card_number_input.clear()
        self.top_up_amount_input.clear()
        dashboard_screen.update_balance()

    def set_current_user(self, username):
        self.current_user = username

    def gotoSettingsScreen(self):
        # Delayed import to resolve circular dependency
        from settings_screen import SettingsScreen

        for index in range(self.stacked_widget.count()):
            widget = self.stacked_widget.widget(index)
            if isinstance(widget, SettingsScreen):
                self.stacked_widget.setCurrentIndex(index)
                break
