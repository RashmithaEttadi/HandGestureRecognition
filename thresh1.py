import cv2
import numpy as np

# Define the RGB threshold values
lower = np.array([0, 20, 70], dtype=np.uint8)
upper = np.array([50, 180, 230], dtype=np.uint8)

# Load the video
cap = cv2.VideoCapture("C:/Users/rashm/Downloads/hand1.mp4")

while True:
    # Read the current frame
    ret, frame = cap.read()
    if not ret:
        break
    
    # Apply the color threshold
    mask = cv2.inRange(frame, lower, upper)
    segmented = cv2.bitwise_and(frame, frame, mask=mask)

    # Display the result
    cv2.imshow("Segmented hand", segmented)

    # Exit if the 'q' key is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
