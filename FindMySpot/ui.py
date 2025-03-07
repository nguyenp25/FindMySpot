import sys
import cv2
import numpy as np
import pickle
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap

# Initialize the parking space positions
try:
    with open('CarParkPos', 'rb') as f:
        posList = pickle.load(f)
except FileNotFoundError:
    posList = []

# Configuration variables
original_width, original_height = 107, 48
scale_percent = 50  # percentage of original size
reserved_spaces = set()  # Set to hold reserved spaces

# Create a Qt application
app = QtWidgets.QApplication(sys.argv)

# Main window class
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Video feed
        self.cap = cv2.VideoCapture('video.mp4')

        # Playback flag
        self.is_paused = False

        # UI setup
        # Modify these lines in the __init__ method of the MainWindow class

        self.setGeometry(100, 100, 2000, 1200)  # Double the width and height

        self.setWindowTitle('FindMySpot')

        # Layouts
        self.layout = QtWidgets.QHBoxLayout()
        self.right_layout = QtWidgets.QVBoxLayout()

        # Image label for displaying the video
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.resize(1280, 960)      # Double the size of the image label
        self.layout.addWidget(self.image_label)

        # Reservation Input
        self.space_input = QtWidgets.QLineEdit(self)
        self.space_input.setPlaceholderText("Enter space number to reserve")
        self.right_layout.addWidget(self.space_input)

        # Reservation Button
        self.reserve_button = QtWidgets.QPushButton("Reserve Space", self)
        self.reserve_button.clicked.connect(self.reserve_space)
        self.right_layout.addWidget(self.reserve_button)

        # Unreserve Button
        self.unreserve_button = QtWidgets.QPushButton("Unreserve", self)
        self.unreserve_button.clicked.connect(self.unreserve_space)
        self.right_layout.addWidget(self.unreserve_button)

        # Information panel
        self.info_panel = QtWidgets.QTextBrowser(self)
        self.right_layout.addWidget(self.info_panel)

        # Add right layout to main layout
        self.layout.addLayout(self.right_layout)

        # Set the layout to the window
        self.setLayout(self.layout)

        # Timer for video updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)  # Update every ~30 ms

        # Pause Button
        self.pause_button = QtWidgets.QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.right_layout.addWidget(self.pause_button)

        # Update info panel
        self.update_info_panel()


    # Method to unreserve a parking space
    def unreserve_space(self):
        try:
            space_number = int(self.space_input.text())
            if 0 <= space_number < len(posList):
                reserved_space = posList[space_number]
                if reserved_space in reserved_spaces:
                    reserved_spaces.remove(reserved_space)
                    self.update_info_panel()
                    self.space_input.clear()
        except ValueError:
            pass

    # Additional method to toggle pause
    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.setText("Resume" if self.is_paused else "Pause")

    def update_frame(self):
        if not self.is_paused:
            ret, frame = self.cap.read()
            if ret:
                # Process the frame
                frame = self.process_frame(frame)

                # Convert frame to QPixmap and display it
                frame_qt = self.convert_cv_qt(frame)
                self.image_label.setPixmap(frame_qt)

    def process_frame(self, frame):
        # Apply image processing to the original frame
        imgGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
        imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                            cv2.THRESH_BINARY_INV, 25, 16)
        imgMedian = cv2.medianBlur(imgThreshold, 5)
        kernel = np.ones((3, 3), np.uint8)
        imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

        # Resize the original frame for display
        scale_factor = scale_percent / 100 * 2  # Double the size
        width_resized = int(frame.shape[1] * scale_factor)
        height_resized = int(frame.shape[0] * scale_factor)
        frame_resized = cv2.resize(frame, (width_resized, height_resized), interpolation=cv2.INTER_AREA)

        free_spaces = len(posList)  # Start with all spaces free
        # Process each parking spot
        for index, pos in enumerate(posList):
            # Scale the coordinates for the resized frame
            x_scaled, y_scaled = int(pos[0] * scale_factor), int(pos[1] * scale_factor)
            width_scaled, height_scaled = int(original_width * scale_factor), int(original_height * scale_factor)

            # Crop from the processed single-channel image (imgDilate)
            imgCrop = imgDilate[pos[1]:pos[1] + original_height, pos[0]:pos[0] + original_width]
            count = cv2.countNonZero(imgCrop)

            # Adjust this threshold based on your specific needs
            threshold = 1400  # Example threshold, adjust this value based on your testing

            if count < threshold:
                if pos in reserved_spaces:
                    color = (0, 255, 255)  # Yellow for reserved spaces
                else:
                    color = (57, 255, 20)  # Green for free spaces
            else:
                color = (0, 0, 255)  # Red for occupied spaces
                free_spaces -= 1

            cv2.rectangle(frame_resized, (x_scaled, y_scaled), (x_scaled + width_scaled, y_scaled + height_scaled), color, 2)

            # Display spot number within the rectangle
            spot_text = f"{index}"
            cv2.putText(frame_resized, spot_text, (x_scaled + 5, y_scaled + height_scaled - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

        # Update free spaces count
        self.info_panel.setText(f"Free spaces: {free_spaces}")
        return frame_resized
    
    def reserve_space(self):
        try:
            space_number = int(self.space_input.text())
            if 0 <= space_number < len(posList):
                reserved_space = posList[space_number]
                if reserved_space not in reserved_spaces:
                    reserved_spaces.add(reserved_space)
                    self.update_info_panel()
                    self.space_input.clear()
        except ValueError:
            pass

    def convert_cv_qt(self, frame):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(convert_to_qt_format)

    def update_info_panel(self):
        self.info_panel.setText("Information Panel\n")

    def reserve_space(self):
        try:
            space_number = int(self.space_input.text())
            if 0 <= space_number < len(posList):
                reserved_spaces.add(posList[space_number])
                self.update_info_panel()
                self.space_input.clear()
        except ValueError:
            pass

    def keyPressEvent(self, event):
        if event.key() == QtGui.QKeySequence('Space'):
            self.is_paused = not self.is_paused
        self.update_info_panel()

    def closeEvent(self, event):
        self.cap.release()

if __name__ == '__main__':
    mw = MainWindow()
    mw.show()
    sys.exit(app.exec_())