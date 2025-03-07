import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from database import Database #Import Database
from settingsScreen import SettingsScreen #Import SettingsScreen
from loginScreen import LoginScreen #Import LoginScreen
from dashboard import DashboardScreen #Import DashboardScreen
from userManagement import UserManagementScreen  # Import UserManagementScreen
from notifications import NotificationsScreen  # Import NotificationsScreen
from paymentInfo import PaymentInformationScreen  # Import PaymentInformationScreen
from parkingPreference import ParkingPreferencesScreen  # Import ParkingPreferencesScreen
from mapSettings import MapSettingsScreen  # Import MapSettingsScreen
from privacySettings import PrivacySettingsScreen  # Import PrivacySettingsScreen
from helpScreen import HelpSupportScreen  # Import HelpAndSupportScreen

class MainApp(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.stacked_widget = QStackedWidget()

        self.database = Database()
        self.loginScreen = LoginScreen(self.stacked_widget, self.database)
        self.dashboard = DashboardScreen(self.stacked_widget)
        # Assuming that SettingsScreen is updated to handle navigation
        self.settingScreen = SettingsScreen(self.stacked_widget, self)
        self.userManagement = UserManagementScreen(self.stacked_widget)
        self.notifications = NotificationsScreen(self.stacked_widget)
        self.paymentInfo = PaymentInformationScreen(self.stacked_widget)
        self.parkingPreference = ParkingPreferencesScreen(self.stacked_widget)
        self.mapSettings = MapSettingsScreen(self.stacked_widget)
        self.privacySettings = PrivacySettingsScreen(self.stacked_widget)
        self.helpScreen = HelpSupportScreen(self.stacked_widget)


             

        self.stacked_widget.addWidget(self.loginScreen)
        self.stacked_widget.addWidget(self.dashboard)
        self.stacked_widget.addWidget(self.settingScreen)
        self.stacked_widget.addWidget(self.userManagement)  # Add UserManagementScreen to QStackedWidget
        self.stacked_widget.addWidget(self.notifications)  # Add NotificationsScreen
        self.stacked_widget.addWidget(self.paymentInfo)
        self.stacked_widget.addWidget(self.parkingPreference)
        self.stacked_widget.addWidget(self.mapSettings)
        self.stacked_widget.addWidget(self.privacySettings)
        self.stacked_widget.addWidget(self.helpScreen)



        self.loadStylesheet("style.qss")
        self.stacked_widget.show()

    def loadStylesheet(self, filename):
        with open(filename, "r") as file:
            self.setStyleSheet(file.read())

if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())