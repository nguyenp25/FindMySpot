import sys
import cv2
import numpy as np
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QPushButton, QStackedWidget, QLabel, QVBoxLayout
from ultralytics import YOLO
from car_parking_detector import ParkingDetector

# Configuration variables
scale_percent = 75
reserved_spaces = set()

app = QtWidgets.QApplication(sys.argv)

class MainWindow(QtWidgets.QWidget):
    def __init__(self, stacked_widget, db, main_app):
        super().__init__()

        self.db = db
        self.main_app = main_app
        self.stacked_widget = stacked_widget
        
        video_path = 'example.mp4'
        weights_path = 'yolov8s.pt'
        spots_file = 'parking_spots.txt'
        self.detector = ParkingDetector(
            video_path, 
            weights_path, 
            spots_file=spots_file, 
            display_scale=scale_percent / 100,
            conf_threshold=0.15,
            iou_threshold=0.5
        )
        self.detector.model = YOLO(weights_path)
        self.detector.model.conf = 0.15
        self.detector.model.iou = 0.5
        
        if not self.detector.spots:
            print("No parking spots loaded. Please define spots using spot_drawer.py first.")
            self.detector.spots = []

        self.is_paused = False
        self.current_user = None
        self.reserved_spots = []
        self.show_cars = False
        self.frame_counter = 0
        self.detection_interval = 0.5

        self.setGeometry(100, 100, int(1920 * 0.8), int(1080 * 0.8))
        self.setWindowTitle('FindMySpot')

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.setSpacing(20)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.setLayout(self.main_layout)

        # Video feed
        self.image_label = QtWidgets.QLabel(self)
        self.image_label.setMinimumSize(int(1920 * 0.6), int(1080 * 0.6))
        self.image_label.setMaximumSize(int(1920 * 0.8), int(1080 * 0.8))
        self.image_label.setScaledContents(True)
        self.image_label.mousePressEvent = self.toggle_car_visibility

        self.overlay_widget = QtWidgets.QWidget(self.image_label)
        self.overlay_widget.setGeometry(10, 10, 200, 60)
        overlay_layout = QtWidgets.QVBoxLayout(self.overlay_widget)
        overlay_layout.setContentsMargins(0, 0, 0, 0)

        self.back_to_dashboard_button = QtWidgets.QPushButton('Back', self.overlay_widget)
        self.back_to_dashboard_button.clicked.connect(self.gotoDashboard)
        overlay_layout.addWidget(self.back_to_dashboard_button, 0, Qt.AlignTop | Qt.AlignLeft)

        self.main_layout.addWidget(self.image_label, stretch=3)
        
        # Right panel layout
        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.setSpacing(15)
        self.right_layout.setContentsMargins(10, 10, 10, 10)

        self.space_input = QtWidgets.QLineEdit(self)
        self.space_input.setPlaceholderText("Enter space number to reserve")
        self.space_input.setMinimumWidth(200)
        self.right_layout.addWidget(self.space_input)

        self.reserve_button = QtWidgets.QPushButton("Reserve Space", self)
        self.reserve_button.clicked.connect(self.reserve_space)
        self.right_layout.addWidget(self.reserve_button)

        self.unreserve_button = QtWidgets.QPushButton("Unreserve", self)
        self.unreserve_button.clicked.connect(self.unreserve_space)
        self.right_layout.addWidget(self.unreserve_button)

        # Info panel with label
        self.info_label = QtWidgets.QLabel("Parking Information", self)
        self.info_label.setObjectName("info_label")
        self.right_layout.addWidget(self.info_label)

        self.info_panel = QtWidgets.QTextBrowser(self)
        self.info_panel.setObjectName("info_panel")
        self.info_panel.setMinimumHeight(200)
        self.right_layout.addWidget(self.info_panel)

        # Notification panel with label
        self.notification_label = QtWidgets.QLabel("Notifications", self)
        self.notification_label.setObjectName("notification_label")
        self.right_layout.addWidget(self.notification_label)

        self.notification_panel = QtWidgets.QTextBrowser(self)
        self.notification_panel.setObjectName("notification_panel")
        self.notification_panel.setMinimumHeight(150)
        self.right_layout.addWidget(self.notification_panel)

        self.pause_button = QtWidgets.QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.toggle_pause)
        self.right_layout.addWidget(self.pause_button)

        self.main_layout.addLayout(self.right_layout, stretch=1)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(33)

        self.update_info_panel()

        # Load QSS stylesheet
        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

    def toggle_car_visibility(self, event):
        self.show_cars = not self.show_cars

    def gotoDashboard(self):
        dashboard_index = self.main_app.widget_indices.get('dashboard_screen')
        if dashboard_index is not None:
            self.main_app.stacked_widget.setCurrentIndex(dashboard_index)

    def set_current_user(self, username):
        self.current_user = username

    def toggle_pause(self):
        self.is_paused = not self.is_paused
        self.pause_button.setText("Resume" if self.is_paused else "Pause")

    def update_frame(self):
        if not self.is_paused:
            ret, frame = self.detector.video.read()
            if ret:
                self.frame_counter += 1
                frame = self.process_frame(frame)
                frame_qt = self.convert_cv_qt(frame)
                self.image_label.setPixmap(frame_qt)
            else:
                self.detector.video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def process_frame(self, frame):
        if self.frame_counter % self.detection_interval == 0:
            frame_enhanced = cv2.convertScaleAbs(frame, alpha=1.2, beta=10)
            results = self.detector.model(frame_enhanced)
            detections = results[0].boxes.data.cpu().numpy()
            car_detections = [d for d in detections if int(d[5]) == 2]

            self.detector.spot_status = {i: False for i in range(len(self.detector.spots))}
            for detection in car_detections:
                x1, y1, x2, y2 = map(int, detection[:4])
                box = (x1, y1, x2, y2)
                spot_indices = self.detector.check_spot_occupation(box)
                for spot_idx in spot_indices:
                    if spot_idx >= 0:
                        self.detector.spot_status[spot_idx] = True
        else:
            car_detections = []

        scale_factor = scale_percent / 100 * 2
        width_resized = int(frame.shape[1] * scale_factor)
        height_resized = int(frame.shape[0] * scale_factor)
        frame_resized = cv2.resize(frame, (width_resized, height_resized), interpolation=cv2.INTER_AREA)

        if self.show_cars and self.frame_counter % self.detection_interval == 0:
            for detection in car_detections:
                x1, y1, x2, y2 = map(int, detection[:4])
                x1_display = int(x1 * scale_factor)
                y1_display = int(y1 * scale_factor)
                x2_display = int(x2 * scale_factor)
                y2_display = int(y2 * scale_factor)
                confidence = float(detection[4])
                
                color = (0, 255, 0) if confidence > 0.5 else (255, 165, 0)
                cv2.rectangle(frame_resized, (x1_display, y1_display), (x2_display, y2_display), color, 2)
                cv2.putText(frame_resized, f'Car {confidence:.2f}', (x1_display, y1_display - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)

        free_spaces = len(self.detector.spots)
        self.reserved_spots = self.db.get_all_reserved_spots()
        for i, spot in enumerate(self.detector.spots):
            scaled_spot = [int(coord * scale_factor) for coord in spot]
            pts = np.array([[scaled_spot[j], scaled_spot[j+1]] for j in range(0, 8, 2)], np.int32)
            pts = pts.reshape((-1, 1, 2))

            if i in self.reserved_spots:
                color = (0, 255, 255)  # Yellow
                free_spaces -= 1
            elif not self.detector.spot_status[i]:
                color = (57, 255, 20)  # Green
            else:
                color = (0, 0, 255)   # Red
                free_spaces -= 1

            cv2.polylines(frame_resized, [pts], True, color, 2)
            spot_center_x = int(sum(scaled_spot[::2]) / 4)
            spot_center_y = int(sum(scaled_spot[1::2]) / 4)
            text = f"Spot {i}"
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 1.0, 3)
            text_x = spot_center_x - text_size[0] // 2
            text_y = spot_center_y + text_size[1] // 2
            cv2.rectangle(frame_resized, 
                          (text_x - 5, text_y - text_size[1] - 5), 
                          (text_x + text_size[0] + 5, text_y + 5), 
                          (50, 50, 50), -1)
            cv2.putText(frame_resized, text, (text_x, text_y),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.0, color, 3)

        self.info_panel.setText(f"Free spaces: {free_spaces}")
        return frame_resized

    def convert_cv_qt(self, frame):
        rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_qt_format = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
        return QPixmap.fromImage(convert_to_qt_format)

    def update_info_panel(self):
        self.info_panel.setText("Parking Information\nShows available spaces and status.")

    def display_notification(self, message):
        current_text = self.notification_panel.toPlainText()
        self.notification_panel.setText(f"{current_text}\n{message}".strip())

    def reserve_space(self):
        try:
            space_number = int(self.space_input.text())
            if 0 <= space_number < len(self.detector.spots):
                username = self.current_user
                dashboard_index = self.main_app.widget_indices.get('dashboard_screen')
                dashboard_screen = self.stacked_widget.widget(dashboard_index)

                if self.db.get_user_balance(username) >= 5:
                    success = self.db.reserve_parking_spot(username, space_number)
                    if success:
                        reserved_spaces.add(tuple(self.detector.spots[space_number]))
                        self.db.update_account_balance(username, -5)
                        if hasattr(dashboard_screen, 'update_dashboard'):
                            dashboard_screen.update_dashboard()
                        self.space_input.clear()
                        self.display_notification("Space reserved successfully.")
                    else:
                        self.display_notification("Space already reserved!")
                else:
                    self.display_notification("Insufficient balance to reserve a space.")
            else:
                self.display_notification("Invalid space number!")
        except ValueError:
            self.display_notification("Invalid input for space number.")

    def unreserve_space(self):
        try:
            space_number = int(self.space_input.text())
            if 0 <= space_number < len(self.detector.spots):
                success = self.db.unreserve_parking_spot(self.current_user, space_number)
                if success:
                    spot_tuple = tuple(self.detector.spots[space_number])
                    if spot_tuple in reserved_spaces:
                        reserved_spaces.remove(spot_tuple)
                    self.update_info_panel()
                    self.space_input.clear()
                    self.db.update_account_balance(self.current_user, 5)
                    dashboard_screen = self.stacked_widget.widget(1)
                    dashboard_screen.update_dashboard()
                    self.display_notification("Space unreserved successfully.")
                else:
                    self.display_notification("You have not reserved this space.")
            else:
                self.display_notification("Invalid space number!")
        except ValueError:
            self.display_notification("Invalid input for space number.")

    def closeEvent(self, event):
        self.detector.video.release()

if __name__ == '__main__':
    from db_module import Database
    db = Database()
    mw = MainWindow(None, db, None)
    mw.show()
    sys.exit(app.exec_())