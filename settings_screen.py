from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton
from user_management_screen import UserManagementScreen
from notifications_screen import NotificationsScreen
from payment_information_screen import PaymentInformationScreen
from parking_preferences_screen import ParkingPreferencesScreen
from privacy_settings_screen import PrivacySettingsScreen
from help_support_screen import HelpScreen


class SettingsScreen(QWidget):
    def __init__(self, stacked_widget, main_app):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.main_app = main_app  # reference to MainApp to access other screens
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Add buttons for settings options
        settings_buttons = [
            ('User Management', 'Edit'),
            ('Payment Information', 'Edit'),
        ]

        for option, button_text in settings_buttons:
            button = QPushButton(f'{option} - {button_text}', self)
            if option == 'User Management':
                button.clicked.connect(self.gotoUserManagementScreen)
            if option == 'Payment Information':
                button.clicked.connect(self.gotoPaymentInformationScreen)
            else:
                button.clicked.connect(self.onButtonClick)
            layout.addWidget(button)
        
        self.back_to_dashboard_button = QPushButton('Back to Dashboard', self)
        self.back_to_dashboard_button.clicked.connect(self.gotoDashboard)
        layout.addWidget(self.back_to_dashboard_button)

        # Set the main layout for the widget
        self.setLayout(layout)

    def onButtonClick(self):
        # Handle button click event for settings options
        sender = self.sender()
        if sender:
            button_text = sender.text()
            print(f'Clicked: {button_text}')

    def gotoUserManagementScreen(self):
        # Switch to the User Management Screen
        index = self.stacked_widget.indexOf(self.main_app.user_management_screen)
        if index != -1:
            self.stacked_widget.setCurrentIndex(index)
        else:
            print("User Management Screen not found in QStackedWidget")

    def gotoNotificationsScreen(self):
        # Switch to the Notifications Screen
        index = self.stacked_widget.indexOf(self.main_app.notifications_screen)
        if index != -1:
            self.stacked_widget.setCurrentIndex(index)
        else:
            print("Notifications Screen not found in QStackedWidget")
    
    def gotoPaymentInformationScreen(self):
        # Switch to the Payment Information Screen
        index = self.stacked_widget.indexOf(self.main_app.payment_information_screen)
        if index != -1:
            self.stacked_widget.setCurrentIndex(index)
        else:
            print("Payment Information Screen not found in QStackedWidget")
    
    def gotoParkingPreferencesScreen(self):
        # Switch to the Parking Preferences Screen
        index = self.stacked_widget.indexOf(self.main_app.parking_preferences_screen)
        if index != -1:
            self.stacked_widget.setCurrentIndex(index)
        else:
            print("Parking Preferences Screen not found in QStackedWidget")
    
    def gotoMapSettingsScreen(self):
        # Switch to the Map Settings Screen
        index = self.stacked_widget.indexOf(self.main_app.map_settings_screen)
        if index != -1:
            self.stacked_widget.setCurrentIndex(index)
        else:
            print("Map Settings Screen not found in QStackedWidget")
    
    def gotoPrivacySettingsScreen(self):
        # Switch to the Privacy Settings Screen
        index = self.stacked_widget.indexOf(self.main_app.privacy_settings_screen)
        if index != -1:
            self.stacked_widget.setCurrentIndex(index)
        else:
            print("Privacy Settings Screen not found in QStackedWidget")

    def gotoHelpAndSupportScreen(self):
        # Switch to the Help and Support Screen
        index = self.stacked_widget.indexOf(self.main_app.help_and_support_screen)
        if index != -1:
            self.stacked_widget.setCurrentIndex(index)
        else:
            print("Help and Support Screen not found in QStackedWidget")    

    def gotoDashboard(self):
        # Switch to the Dashboard Screen
        index = self.stacked_widget.indexOf(self.main_app.dashboard_screen)
        if index != -1:
            self.stacked_widget.setCurrentIndex(index)
        else:
            print("Dashboard Screen not found in QStackedWidget")

    # Additional methods to handle navigation to other screens as needed
    # Example:
    # def gotoNotificationsScreen(self):
    #     # Logic to navigate to the Notifications screen
