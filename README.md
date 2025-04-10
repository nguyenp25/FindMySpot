# FindMySpot
Senior Project for Wentworth

# FindMySpot

**FindMySpot** is a smart parking management app that uses computer vision and a PyQt5 GUI to monitor parking availability in real-time, allowing users to reserve spots effortlessly.

## Features
- Real-Time Parking Detection: Identifies occupied spots with YOLOv8m and OpenCV.
- Interactive GUI: Shows live spot statuses (green = free, red = occupied, yellow = reserved).
- Spot Reservations: Reserve/unreserve spots with balance authentication.
- User Management: Login/register and balance tracking via MongoDB.
- Notifications: In-app feedback 
- Optimized Performance: Frame skipping and 1.5x video scaling.

## Technical Implementation
- Computer Vision (OpenCV):
  - Reads video (`cv2.VideoCapture`), resizes frames (`cv2.resize`).
  - Enhances lighting (`cv2.convertScaleAbs`), draws spots/numbers (`cv2.polylines`, `cv2.putText`).
- Object Detection (YOLOv8):
  - Uses `yolov8m`, optimized to run every 5th frame.
- Database (MongoDB):
  - Stores user data (balance, reservations); spots from `parking_spots.txt`.
- Front-End (PyQt5 GUI):
  - Live map (`QLabel`) with toggled car visibility, real-time free spaces, and notifications.

## Requirements
- Software:
  - Python 3.8+
  - MongoDB running locally
- Python Packages:
  - opencv-python: For video processing and drawing.
  - ultralytics: YOLOv8m model for car detection.
  - pymongo: MongoDB integration.
  - pyqt5: GUI framework.
- Files:
  - video.mp4: Input video of the parking lot.
  - yolov8m.pt: Pre-trained YOLOv8m weights.
  - parking_spots.txt: Spot coordinates (format: `x1,y1,x2,y2,x3,y3,x4,y4` per line).
- Hardware (Recommended):
  - CPU: Multi-core for YOLO processing.
  - RAM: 8GB+ for smooth video handling.
  - Optional: GPU (NVIDIA) for faster YOLO inference.

### Setup
- Clone the Repository:
  ```
  git clone https://github.com/yourusername/FindMySpot.git
  cd FindMySpot

- Configure Files:
  - Add video.mp4 to the root directory.
  - Create parking_spots.txt with spot coordinates (e.g., 100,100,200,100,200,200,100,200).
  - Download yolov8m.pt from Ultralytics and place in root.
  - Create signalwire_config.py (see SignalWire Integration).
  - Run the App
