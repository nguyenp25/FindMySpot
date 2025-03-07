from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class ParkingPreferencesScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label = QLabel("Parking Preferences Settings", self)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)