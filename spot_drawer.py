import cv2
import numpy as np

class ParkingSpotDrawer:
    def __init__(self, video_path):
        self.video = cv2.VideoCapture(video_path)
        if not self.video.isOpened():
            raise ValueError(f"Could not open video file: {video_path}")
        
        ret, self.frame = self.video.read()
        if not ret:
            raise ValueError("Could not read first frame from video")
        
        self.points = []
        self.current_spot = []
        self.spots = []

    def draw_spot(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.current_spot.append((x, y))
            cv2.circle(self.frame, (x, y), 5, (0, 255, 0), -1)
            
            # If we have 4 points, complete the spot
            if len(self.current_spot) == 4:
                self.spots.append([coord for point in self.current_spot for coord in point])  # Flatten to [x1,y1,x2,y2,x3,y3,x4,y4]
                # Draw the polygon
                pts = np.array(self.current_spot, np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(self.frame, [pts], True, (0, 255, 0), 2)
                self.current_spot = []  # Reset for next spot
                
            cv2.imshow('Draw Parking Spots', self.frame)

    def run(self):
        # Create a resizable window
        cv2.namedWindow('Draw Parking Spots', cv2.WINDOW_NORMAL)
        # Optional: Set initial window size (width, height)
        cv2.resizeWindow('Draw Parking Spots', 800, 600)
        cv2.setMouseCallback('Draw Parking Spots', self.draw_spot)
        
        print("Click 4 corners for each parking spot. Press 's' to save and quit, 'q' to quit without saving.")
        
        while True:
            cv2.imshow('Draw Parking Spots', self.frame)
            key = cv2.waitKey(1) & 0xFF
            
            if key == ord('s'):  # Save and exit
                self.save_spots()
                break
            elif key == ord('q'):  # Quit without saving
                break
        
        self.video.release()
        cv2.destroyAllWindows()
        return self.spots

    def save_spots(self, filename='parking_spots.txt'):
        with open(filename, 'w') as f:
            for spot in self.spots:
                f.write(','.join(map(str, spot)) + '\n')
        print(f"Saved {len(self.spots)} parking spots to {filename}")

if __name__ == "__main__":
    video_path = 'example.mp4'  # Replace with your video path
    try:
        drawer = ParkingSpotDrawer(video_path)
        spots = drawer.run()
        print("Defined spots:", spots)
    except ValueError as e:
        print(f"Error: {e}")