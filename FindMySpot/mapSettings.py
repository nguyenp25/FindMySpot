from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class MapSettingsScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label = QLabel("Map Settings", self)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)