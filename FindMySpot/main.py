import sys
from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtCore import Qt, QCoreApplication

#FindMySpot

# Set the attribute before creating the QApplication instance
QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)

# Now import the module that requires the attribute to be set
from PyQt5.QtWebEngineWidgets import QWebEngineView

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
from ui import MainWindow # Import Main UI Screen


class MainApp(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.stacked_widget = QStackedWidget()
        self.widget_indices = {}
        
        self.database = Database()
        
        # Initialize and add your screens
        self.loginScreen = LoginScreen(self.stacked_widget, self.database)
        self.widget_indices['loginScreen'] = self.stacked_widget.addWidget(self.loginScreen)

        self.dashboard = DashboardScreen(self.stacked_widget)
        self.widget_indices['dashboard'] = self.stacked_widget.addWidget(self.dashboard)

        self.settingScreen = SettingsScreen(self.stacked_widget, self)
        self.widget_indices['settingScreen'] = self.stacked_widget.addWidget(self.settingScreen)

        self.userManagement = UserManagementScreen(self.stacked_widget)
        self.widget_indices['userManagement'] = self.stacked_widget.addWidget(self.userManagement)

        self.notifications = NotificationsScreen(self.stacked_widget)
        self.widget_indices['notifications'] = self.stacked_widget.addWidget(self.notifications)

        self.paymentInfo = PaymentInformationScreen(self.stacked_widget)
        self.widget_indices['paymentInfo'] = self.stacked_widget.addWidget(self.paymentInfo)

        self.parkingPreference = ParkingPreferencesScreen(self.stacked_widget)
        self.widget_indices['parkingPreference'] = self.stacked_widget.addWidget(self.parkingPreference)

        self.mapSettings = MapSettingsScreen(self.stacked_widget)
        self.widget_indices['mapSettings'] = self.stacked_widget.addWidget(self.mapSettings)

        self.privacySettings = PrivacySettingsScreen(self.stacked_widget)
        self.widget_indices['privacySettings'] = self.stacked_widget.addWidget(self.privacySettings)

        self.helpScreen = HelpSupportScreen(self.stacked_widget)
        self.widget_indices['helpScreen'] = self.stacked_widget.addWidget(self.helpScreen)

        self.mainWindow = MainWindow(self.database)
        self.widget_indices['mainWindow'] = self.stacked_widget.addWidget(self.mainWindow)

        self.loadStylesheet("style.qss")
        self.stacked_widget.show()

    def loadStylesheet(self, filename):
        with open(filename, "r") as file:
            self.setStyleSheet(file.read())

if __name__ == '__main__':
    app = MainApp(sys.argv)
    sys.exit(app.exec_())
    