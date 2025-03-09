from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QDesktopServices
from camera import MainWindow

class DashboardScreen(QWidget):
    def __init__(self, stacked_widget, widget_indices, db, current_user):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.widget_indices = widget_indices
        self.db = db
        self.current_user = current_user
        layout = QVBoxLayout(self)

        # Header label with object name for QSS targeting
        self.dashboard_label = QLabel('           Dashboard - Reservations', self)
        self.dashboard_label.setObjectName("dashboard_label")  # Matches #dashboard_label in QSS
        layout.addWidget(self.dashboard_label)

        # Balance label with object name
        self.balance_label = QLabel('Balance: $0', self)
        self.balance_label.setObjectName("balance_label")  # Matches #balance_label in QSS
        layout.addWidget(self.balance_label)

        # Buttons for navigation
        self.ui_button = QPushButton('Camera', self)
        self.ui_button.clicked.connect(self.gotoUI)
        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.gotoSettings)
        self.logout_button = QPushButton('Logout', self)
        self.logout_button.clicked.connect(self.logout)

        # Button layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ui_button)
        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.logout_button)
        layout.addLayout(button_layout)

        # Table for reservations
        self.reservation_table = QTableWidget(0, 1)
        self.reservation_table.setHorizontalHeaderLabels(['Reserved Spots'])
        self.reservation_table.setObjectName("reservation_table")  # For QSS targeting
        header = self.reservation_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.reservation_table.setAlternatingRowColors(True)
        layout.addWidget(self.reservation_table)
        self.update_reservations()

        self.setLayout(layout)
        self.setWindowTitle('Dashboard')

    def set_current_user(self, username):
        self.current_user = username

    def update_balance(self):
        balance = self.db.get_user(self.current_user)['balance']
        self.balance_label.setText(f'Balance: ${balance}')

    def update_dashboard(self):
        self.update_reservations()
        self.update_balance()

    def update_reservations(self):
        user_reservations = self.db.get_user_reservations(self.current_user)
        self.reservation_table.setRowCount(len(user_reservations))
        for row, spot_id in enumerate(user_reservations):
            self.reservation_table.setItem(row, 0, QTableWidgetItem(str(spot_id)))

    def gotoSettings(self):
        self.stacked_widget.setCurrentIndex(2)

    def logout(self):
        self.stacked_widget.setCurrentIndex(0)

    def gotoUI(self):
        main_window_index = self.widget_indices.get('main_window')
        if main_window_index is not None:
            self.stacked_widget.setCurrentIndex(main_window_index)