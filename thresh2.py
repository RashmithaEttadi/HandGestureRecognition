import cv2
import numpy as np

# Define the HSV threshold values
lower_hsv = np.array([0, 20, 70], dtype=np.uint8)
upper_hsv = np.array([30, 255, 255], dtype=np.uint8)

# Load the video
cap = cv2.VideoCapture("C:/Users/rashm/Downloads/hand1.mp4")

while True:
    # Read the current frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    # Apply the color threshold
    mask = cv2.inRange(hsv, lower_hsv, upper_hsv)
    segmented = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the result
    cv2.imshow("Segmented hand", segmented)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
