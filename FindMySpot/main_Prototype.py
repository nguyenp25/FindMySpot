import cv2
import pickle
import cvzone
import numpy as np

# Video feed
cap = cv2.VideoCapture('Park.mp4')

with open('CarParkPos', 'rb') as f:
    posList = pickle.load(f)

original_width, original_height = 107, 48
scale_percent = 50  # percentage of original size

# Playback flag
is_paused = False  # Start with playback not paused

def checkParkingSpace(imgPro, imgDisplay):
    spaceCounter = 0

    for index,pos in enumerate(posList):
        x, y = pos

        imgCrop = imgPro[y:y + original_height, x:x + original_width]
        count = cv2.countNonZero(imgCrop)
        # Adjust this threshold based on your specific needs
        if index in [30, 32, 42, 43]:
            threshold = 1500
        else:
            threshold = 1200

        if count < threshold:
            color = (0, 255, 0)
            thickness = 5
            spaceCounter += 1
        else:
            color = (0, 0, 255)
            thickness = 2

        # Scale the position for the resized image
        x_scaled, y_scaled = int(x * scale_percent / 100), int(y * scale_percent / 100)
        width_scaled, height_scaled = int(original_width * scale_percent / 100), int(original_height * scale_percent / 100)

        cv2.rectangle(imgDisplay, (x_scaled, y_scaled), (x_scaled + width_scaled, y_scaled + height_scaled), color, thickness)
        cvzone.putTextRect(imgDisplay, str(count), (x_scaled, y_scaled + height_scaled - 3), scale=1,
                           thickness=2, offset=0, colorR=color)

    cvzone.putTextRect(imgDisplay, f'Free: {spaceCounter}/{len(posList)}', (100, 50), scale=1.5,
                       thickness=2, offset=20, colorR=(0,200,0))

while True:
    # Only read new frame if the video is not paused
    if not is_paused:
        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        success, img = cap.read()
        if not success:
            break

    # Image processing to create imgDilate
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (3, 3), 1)
    imgThreshold = cv2.adaptiveThreshold(imgBlur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                         cv2.THRESH_BINARY_INV, 25, 16)
    imgMedian = cv2.medianBlur(imgThreshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    imgDilate = cv2.dilate(imgMedian, kernel, iterations=1)

    # Resize the original frame before drawing rectangles and displaying it
    width_resized = int(img.shape[1] * scale_percent / 100)
    height_resized = int(img.shape[0] * scale_percent / 100)
    img_display = cv2.resize(img, (width_resized, height_resized), interpolation=cv2.INTER_AREA)

    # Now pass the dilated image for processing and the resized image for drawing rectangles
    checkParkingSpace(imgDilate, img_display)

    # Display the resized frame with rectangles
    cv2.imshow("Image", img_display)
    # Check for keypresses
    key = cv2.waitKey(10)

    if key & 0xFF == ord('q'):
        break
    elif key & 0xFF == 32:  # Spacebar ASCII code
        is_paused = not is_paused  # Toggle pause

cap.release()
cv2.destroyAllWindows()


# Cleanup
cap.release()
cv2.destroyAllWindows()
