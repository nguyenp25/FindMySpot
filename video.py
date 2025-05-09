import cv2
import numpy as np
from ultralytics import YOLO
import imageio

class ParkingDetector:
    def __init__(self, video_path, weights_path, spots_file='', display_scale=0.25, conf_threshold=0.7, iou_threshold=0.7):
        # Load YOLOv8 model
        self.model = YOLO(weights_path)
        self.video = cv2.VideoCapture(video_path)
        if not self.video.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        self.spots = self.load_spots(spots_file)
        self.spot_status = {i: False for i in range(len(self.spots))}
        self.display_scale = display_scale
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
            print(f"Warning: {filename} not found. No parking spots loaded.")
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

    def process_and_save_gif(self, output_path, duration=5):
        # Get video properties
        frame_width = int(self.video.get(cv2.CAP_PROP_FRAME_WIDTH) * self.display_scale)
        frame_height = int(self.video.get(cv2.CAP_PROP_FRAME_HEIGHT) * self.display_scale)
        fps = int(self.video.get(cv2.CAP_PROP_FPS))
        
        # Use a reduced frame rate for GIF (e.g., 15 FPS)
        gif_fps = 15
        # Calculate max frames for the given duration at reduced FPS
        max_frames = gif_fps * duration
        frame_count = 0
        frames = []
        
        print(f"Processing first {duration} seconds of video at {gif_fps} FPS and saving as GIF to {output_path}...")
        
        while self.video.isOpened() and frame_count < max_frames:
            ret, frame = self.video.read()
            if not ret:
                print("End of video or error reading frame")
                break
                
            # Skip frames to match reduced FPS (e.g., take every 2nd frame if input is 30 FPS)
            if frame_count % (fps // gif_fps) != 0:
                continue
                
            # Resize frame for processing
            display_frame = cv2.resize(frame, (frame_width, frame_height), interpolation=cv2.INTER_AREA)
            
            # YOLOv8 detection
            results = self.model(frame, conf=self.conf_threshold, iou=self.iou_threshold)
            car_detections = [box for box in results[0].boxes if int(box.cls) == 2]  # Class 2 is 'car' in COCO
            
            # Reset spot status
            self.spot_status = {i: False for i in range(len(self.spots))}
            
            # Draw car detections
            for detection in car_detections:
                x1, y1, x2, y2 = map(int, detection.xyxy[0])
                box = (x1, y1, x2, y2)
                spot_indices = self.check_spot_occupation(box)
                
                for spot_idx in spot_indices:
                    if spot_idx >= 0:
                        self.spot_status[spot_idx] = True
                
                # Scale coordinates for display
                x1_display = int(x1 * self.display_scale)
                y1_display = int(y1 * self.display_scale)
                x2_display = int(x2 * self.display_scale)
                y2_display = int(y2 * self.display_scale)
                confidence = float(detection.conf)
                
                # Draw car bounding box and label
                cv2.rectangle(display_frame, (x1_display, y1_display), (x2_display, y2_display), (0, 255, 0), 1)
                cv2.putText(display_frame, f'Car {confidence:.2f}', (x1_display, y1_display-5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
            
            # Draw parking spots
            for i, spot in enumerate(self.spots):
                color = (0, 255, 0) if not self.spot_status[i] else (0, 0, 255)
                scaled_spot = [int(coord * self.display_scale) for coord in spot]
                pts = np.array([[scaled_spot[j], scaled_spot[j+1]] for j in range(0, 8, 2)], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(display_frame, [pts], True, color, 1)
                cv2.putText(display_frame, f"Spot {i}: {'Occupied' if self.spot_status[i] else 'Free'}",
                           (scaled_spot[0], scaled_spot[1]-5), cv2.FONT_HERSHEY_SIMPLEX, 0.4, color, 1)
            
            # Convert BGR to RGB and append to frames list
            display_frame_rgb = cv2.cvtColor(display_frame, cv2.COLOR_BGR2RGB)
            frames.append(display_frame_rgb)
            frame_count += 1
        
        # Save frames as GIF
        imageio.mimsave(output_path, frames, fps=gif_fps)
        
        # Release resources
        self.video.release()
        print(f"GIF saved to {output_path} with {len(frames)} frames, estimated size < 50 MB")

if __name__ == "__main__":
    # Input and output paths
    video_path = 'example.mp4'
    weights_path = 'yolov8m.pt'
    output_path = 'output_detections.gif'
    
    try:
        detector = ParkingDetector(video_path, weights_path, display_scale=0.25, conf_threshold=0.4, iou_threshold=0.6)
        detector.process_and_save_gif(output_path, duration=5)
    except ValueError as e:
        print(f"Error: {e}")