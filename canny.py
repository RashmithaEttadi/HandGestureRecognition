import cv2

# Load video file
cap = cv2.VideoCapture(0)

# Create a Haar cascade classifier for hand detection
hand_cascade = cv2.CascadeClassifier("C:/Users/rashm/Downloads/haarcascade_frontalface_default.xml")

while True:
    # Read the current frame from the video
    ret, frame = cap.read()

    # Check if the video has ended
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply Canny edge detection algorithm
    edges = cv2.Canny(gray, 50, 150)

    # Detect hands using Haar cascade classifier
    hands = hand_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw rectangles around the detected hands
    for (x,y,w,h) in hands:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

    # Display the frame with detected hands and edges
    cv2.imshow('frame', frame)
    cv2.imshow('edges', edges)

    # Press 'q' key to exit
    if cv2.waitKey(1) == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
