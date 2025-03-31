from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QHeaderView, QHBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, QTimer, Qt, QRect
from PyQt5.QtGui import QDesktopServices, QPalette, QColor
from PyQt5.QtWidgets import QMessageBox
from camera import MainWindow

class DashboardScreen(QWidget):
    def __init__(self, stacked_widget, widget_indices, db, current_user):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.widget_indices = widget_indices
        self.db = db
        self.current_user = current_user
        layout = QVBoxLayout(self)

        header_layout = QHBoxLayout()
        
        self.dashboard_label = QLabel('           Dashboard - Reservations', self)
        self.dashboard_label.setObjectName("dashboard_label")
        header_layout.addWidget(self.dashboard_label, stretch=1)
        
        layout.addLayout(header_layout)

        self.balance_label = QLabel('Balance: $0', self)
        self.balance_label.setObjectName("balance_label")
        layout.addWidget(self.balance_label)

        self.ui_button = QPushButton('Camera', self)
        self.ui_button.clicked.connect(self.gotoUI)
        self.settings_button = QPushButton('Settings', self)
        self.settings_button.clicked.connect(self.gotoSettings)
        self.logout_button = QPushButton('Logout', self)
        self.logout_button.clicked.connect(self.logout)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ui_button)
        button_layout.addWidget(self.settings_button)
        button_layout.addWidget(self.logout_button)
        layout.addLayout(button_layout)

        self.reservation_table = QTableWidget(0, 2)
        self.reservation_table.setHorizontalHeaderLabels(['Reserved Spots', 'Time Remaining'])
        self.reservation_table.setObjectName("reservation_table")
        header = self.reservation_table.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.Stretch)
        self.reservation_table.setAlternatingRowColors(True)
        layout.addWidget(self.reservation_table)

        # Moved timer and active_spot initialization before update_reservations()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_reservation_times)
        self.active_spot = None
        self.popup_shown = False

        self.update_reservations()  # Now safe to call after active_spot is defined

        self.setLayout(layout)
        self.setWindowTitle('Dashboard')

    def start_reservation_timer(self, spot_id):
        self.active_spot = spot_id
        self.popup_shown = False
        self.update_reservations()
        if not self.timer.isActive():
            self.timer.start(1000)

    def update_reservation_times(self):
        if self.active_spot is None:
            self.timer.stop()
            return

        remaining_seconds = self.db.get_remaining_time(self.active_spot)
        if remaining_seconds > 0:
            minutes = remaining_seconds // 60
            seconds = remaining_seconds % 60
            for row in range(self.reservation_table.rowCount()):
                if self.reservation_table.item(row, 0).text() == str(self.active_spot):
                    time_item = QTableWidgetItem(f'{minutes:02d}:{seconds:02d}')
                    time_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.reservation_table.setItem(row, 1, time_item)
                    if remaining_seconds == 3 and not self.popup_shown:
                        self.popup_shown = True
                        # Show notification popup when 3 seconds remain
                        self.show_notification(
                            "Reservation Expiring Soon",
                            f"Your reservation for parking spot {self.active_spot} is expiring in 1 minute."
                        )
        else:
            self.db.unreserve_parking_spot(self.current_user, self.active_spot)
            self.active_spot = None
            self.popup_shown = False
            self.update_reservations()



    def update_dashboard(self):
        self.update_reservations()
        self.update_balance()
        if self.active_spot is not None:
            self.update_reservation_times()

    def set_current_user(self, username):
        self.current_user = username

    def update_balance(self):
        balance = self.db.get_user(self.current_user)['balance']
        self.balance_label.setText(f'Balance: ${balance}')

    def update_reservations(self):
        user_reservations = self.db.get_user_reservations(self.current_user)
        self.reservation_table.setRowCount(len(user_reservations))
        for row, spot_id in enumerate(user_reservations):
            self.reservation_table.setItem(row, 0, QTableWidgetItem(str(spot_id)))
            if self.active_spot is not None and spot_id == self.active_spot:
                remaining_seconds = self.db.get_remaining_time(spot_id)
                if remaining_seconds > 0:
                    minutes = remaining_seconds // 60
                    seconds = remaining_seconds % 60
                    time_item = QTableWidgetItem(f'{minutes:02d}:{seconds:02d}')
                    time_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.reservation_table.setItem(row, 1, time_item)
                else:
                    time_item = QTableWidgetItem('Expired')
                    time_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                    self.reservation_table.setItem(row, 1, time_item)
                    self.active_spot = None
            else:
                time_item = QTableWidgetItem('N/A')
                time_item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
                self.reservation_table.setItem(row, 1, time_item)

    def gotoSettings(self):
        self.stacked_widget.setCurrentIndex(2)

    def logout(self):
        self.stacked_widget.setCurrentIndex(0)

    def gotoUI(self):
        main_window_index = self.widget_indices.get('main_window')
        if main_window_index is not None:
            self.stacked_widget.setCurrentIndex(main_window_index)
            
    def show_notification(self, title, message):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText(message)
        msg.setWindowTitle(title)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()
