from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton

class SettingsScreen(QWidget):
    def __init__(self, stacked_widget, dashboard_index=1):
        super().__init__()
        self.stacked_widget = stacked_widget
        self.dashboard_index = dashboard_index
        self.initUI()

    def initUI(self):
        # Create a QVBoxLayout for the main layout
        layout = QVBoxLayout()

        # Add buttons for settings options
        settings_buttons = [
            ('User Management', 'Edit'),
            ('Notifications', 'Edit'),
            ('Payment Information', 'Edit'),
            ('Parking Preferences', 'Edit'),
            ('Map Settings', 'Edit'),
            ('Privacy Settings', 'Edit'),
            ('Help and Support', 'Edit')
        ]

        for option, button_text in settings_buttons:
            button = QPushButton(f'{option} - {button_text}', self)
            button.clicked.connect(self.onButtonClick)
            layout.addWidget(button)

        # Add a back button
        back_button = QPushButton('Back to Dashboard', self)
        back_button.clicked.connect(self.gotoDashboard)
        layout.addWidget(back_button)

        # Set the main layout for the widget
        self.setLayout(layout)

    def onButtonClick(self):
        # Handle button click event for settings options
        sender = self.sender()
        if sender:
            button_text = sender.text()
            print(f'Clicked: {button_text}')

    def gotoDashboard(self):
        # Change the current widget of the stacked_widget to Dashboard
        self.stacked_widget.setCurrentIndex(self.dashboard_index)