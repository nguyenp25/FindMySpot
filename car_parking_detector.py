# car_parking_detector.py
import cv2
import numpy as np
from ultralytics import YOLO

class ParkingDetector:
    def __init__(self, video_path, weights_path, spots_file='parking_spots.txt', display_scale=0.5, conf_threshold=0.2, iou_threshold=0.1):
        # Load YOLOv8 model instead of YOLOv5
        self.model = YOLO(weights_path)
        self.video = cv2.VideoCapture(video_path)
        if not self.video.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        self.spots = self.load_spots(spots_file)
        self.spot_status = {i: False for i in range(len(self.spots))}
        self.display_scale = display_scale
        self.show_cars = True
        self.conf_threshold = conf_threshold
        self.iou_threshold = iou_threshold

    def load_spots(self, filename):
        spots = []
        try:
            with open(filename, 'r') as f:
                for line in f:
                    points = list(map(int, line.strip().split(',')))
                    if len(points) == 8:
                        spots.append(points)
        except FileNotFoundError:
            print(f"Warning: {filename} not found. Please define spots first.")
        return spots

    def intersect_area(self, box, spot):
        spot_x = [spot[i] for i in range(0, 8, 2)]
        spot_y = [spot[i] for i in range(1, 8, 2)]
        spot_x1, spot_y1 = min(spot_x), min(spot_y)
        spot_x2, spot_y2 = max(spot_x), max(spot_y)
        
        box_x1, box_y1, box_x2, box_y2 = box
        
        inter_x1 = max(box_x1, spot_x1)
        inter_y1 = max(box_y1, spot_y1)
        inter_x2 = min(box_x2, spot_x2)
        inter_y2 = min(box_y2, spot_y2)
        
        if inter_x1 < inter_x2 and inter_y1 < inter_y2:
            inter_area = (inter_x2 - inter_x1) * (inter_y2 - inter_y1)
            box_area = (box_x2 - box_x1) * (box_y2 - box_y1)
            spot_area = (spot_x2 - spot_x1) * (spot_y2 - spot_y1)
            return inter_area / min(box_area, spot_area)
        return 0.0

    def check_spot_occupation(self, box):
        x1, y1, x2, y2 = box
        occupied_spots = []
        
        for i, spot in enumerate(self.spots):
            overlap = self.intersect_area(box, spot)
            if overlap > 0.5:
                occupied_spots.append(i)
        
        return occupied_spots if occupied_spots else [-1]

    def detect(self):
        cv2.namedWindow('Parking Detection', cv2.WINDOW_NORMAL)
        print("Press 't' to toggle car detection visibility, 'q' to quit")
        
        while self.video.isOpened():
            ret, frame = self.video.read()
            if not ret:
                print("End of video or error reading frame")
                break
                
            height, width = frame.shape[:2]
            new_width = int(width * self.display_scale)
            new_height = int(height * self.display_scale)
            display_frame = cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)
            
            # YOLOv8 detection with specified confidence and iou thresholds
            results = self.model(frame, conf=self.conf_threshold, iou=self.iou_threshold)
            # Filter for cars (class 2 in COCO dataset)
            car_detections = [box for box in results[0].boxes if int(box.cls) == 2]
            
            self.spot_status = {i: False for i in range(len(self.spots))}
            
            for detection in car_detections:
                # YOLOv8 returns xyxy format directly
                x1, y1, x2, y2 = map(int, detection.xyxy[0])
                box = (x1, y1, x2, y2)
                spot_indices = self.check_spot_occupation(box)
                
                for spot_idx in spot_indices:
                    if spot_idx >= 0:
                        self.spot_status[spot_idx] = True
                
                if self.show_cars:
                    x1_display = int(x1 * self.display_scale)
                    y1_display = int(y1 * self.display_scale)
                    x2_display = int(x2 * self.display_scale)
                    y2_display = int(y2 * self.display_scale)
                    confidence = float(detection.conf)
                    
                    cv2.rectangle(display_frame, (x1_display, y1_display), (x2_display, y2_display), (0, 255, 0), 2)
                    cv2.putText(display_frame, f'Car {confidence:.2f}', (x1_display, y1_display-10),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            
            for i, spot in enumerate(self.spots):
                color = (0, 255, 0) if not self.spot_status[i] else (0, 0, 255)
                scaled_spot = [int(coord * self.display_scale) for coord in spot]
                pts = np.array([[scaled_spot[j], scaled_spot[j+1]] for j in range(0, 8, 2)], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(display_frame, [pts], True, color, 2)
                cv2.putText(display_frame, f"Spot {i}: {'Occupied' if self.spot_status[i] else 'Available'}",
                           (scaled_spot[0], scaled_spot[1]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            cv2.imshow('Parking Detection', display_frame)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('t'):
                self.show_cars = not self.show_cars
                print(f"Car detection visibility: {'ON' if self.show_cars else 'OFF'}")
        
        self.video.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    video_path = 'Park3.mp4'
    weights_path = 'yolov8m.pt'
    try:
        detector = ParkingDetector(video_path, weights_path, display_scale=0.5, conf_threshold=0.4, iou_threshold=0.6)
        detector.detect()
    except ValueError as e:
        print(f"Error: {e}")