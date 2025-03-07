from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout

class PaymentInfoScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        label = QLabel("Payment Information Settings", self)
        layout = QVBoxLayout()
        layout.addWidget(label)
        self.setLayout(layout)