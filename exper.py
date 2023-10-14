import cv2
import numpy as np
import math
import pyautogui

# open the video file
cap = cv2.VideoCapture(0)

# create a window to display the frames
cv2.namedWindow('Hand Detection')

# create trackbars to adjust the lower and upper thresholds for the skin color detection
def nothing(x):
    pass

cv2.createTrackbar('Hue Lower', 'Hand Detection', 0, 255, nothing)
cv2.createTrackbar('Saturation Lower', 'Hand Detection', 20, 255, nothing)
cv2.createTrackbar('Value Lower', 'Hand Detection', 70, 255, nothing)
cv2.createTrackbar('Hue Upper', 'Hand Detection', 20, 255, nothing)
cv2.createTrackbar('Saturation Upper', 'Hand Detection', 255, 255, nothing)
cv2.createTrackbar('Value Upper', 'Hand Detection', 255, 255, nothing)

# Define constant values
MIN_ANGLE_THRESHOLD = 90
MIN_DISTANCE_THRESHOLD = 30

def detect_fingers(defects, approx, roi):
    """
    Detect fingers in an image of a hand.
    """
    finger_count = 0
    for i in range(defects.shape[0]):
        start_idx, end_idx, far_idx, _ = defects[i, 0]
        start = tuple(approx[start_idx][0])
        end = tuple(approx[end_idx][0])
        far = tuple(approx[far_idx][0])
        point = (100, 180)

        # Calculate lengths of sides of the triangle formed by the three points
        side_a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
        side_b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
        side_c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)

        # Calculate semiperimeter and area of triangle
        semiperimeter = (side_a + side_b + side_c) / 2
        area = math.sqrt(semiperimeter * (semiperimeter - side_a) * (semiperimeter - side_b) * (semiperimeter - side_c))

        # Calculate distance between point and convex hull
        distance = (2 * area) / side_a

        # Calculate angle between sides a and c
        cos_angle = (side_b ** 2 + side_c ** 2 - side_a ** 2) / (2 * side_b * side_c)
        angle = math.acos(cos_angle) * 57

        # Ignore angles greater than 90 degrees and points too close to the convex hull
        if angle <= MIN_ANGLE_THRESHOLD and distance > MIN_DISTANCE_THRESHOLD:
            finger_count += 1
            cv2.circle(roi, far, 3, [255, 0, 0], -1)

        # Draw lines around hand
        cv2.line(roi, start, end, [0, 255, 0], 2)
        
    finger_count= finger_count+1

    return finger_count
def display_finger_count(areacnt, arearatio, finger_count):
    if finger_count==1:
        if areacnt<2000:
            return 'Place hand in box'
        else:
            if arearatio<12:
                pyautogui.press('0 ')
                return '0'
            elif arearatio<17.5:
                pyautogui.press('Best of luck ')
                return 'Best of luck'
            else:
                pyautogui.press('1 ')
                return '1'
    elif finger_count==2:
        pyautogui.press('2 ')
        return '2'
    elif finger_count==3:
        if arearatio<27:
            pyautogui.press('3 ')
            return '3'
        else:
            pyautogui.press('ok ')
            return 'ok'
    elif finger_count==4:
        pyautogui.press('4 ')
        return '4'
    elif finger_count==5:
        pyautogui.press('5 ')
        return '5'
    else :
        return 'reposition'


while(cap.isOpened()):
    try:
    # read the next frame from the video file
        ret, frame = cap.read()
        if ret == False:
            break

    # flip the frame horizontally
        frame = cv2.flip(frame, 1)

    # define region of interest
        roi = frame[100:300, 100:300]

        cv2.rectangle(frame,(100,100),(300,300),(0,255,0),0) 

    # get the trackbar values for the lower and upper thresholds
        h_l = cv2.getTrackbarPos('Hue Lower', 'Hand Detection')
        s_l = cv2.getTrackbarPos('Saturation Lower', 'Hand Detection')
        v_l = cv2.getTrackbarPos('Value Lower', 'Hand Detection')
        h_u = cv2.getTrackbarPos('Hue Upper', 'Hand Detection')
        s_u = cv2.getTrackbarPos('Saturation Upper', 'Hand Detection')
        v_u = cv2.getTrackbarPos('Value Upper', 'Hand Detection')

    # define range of skin color in HSV
        lower_skin = np.array([h_l, s_l, v_l], dtype=np.uint8)
        upper_skin = np.array([h_u, s_u, v_u], dtype=np.uint8)

    # extract skin color image  
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # extrapolate the hand to fill dark spots within
        kernel = np.ones((3,3), np.uint8)
        dilation = cv2.dilate(mask, kernel, iterations=4) 
        erosion = cv2.erode(dilation, kernel, iterations=4)

    # blur the image
        mask = cv2.GaussianBlur(mask, (5,5), 100) 

    # find contours
        contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # find all contours with a significant area
        significant_contours = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 500:
                significant_contours.append(cnt)

   #find contour of max area(hand)
        cnt = max(significant_contours, key = lambda x: cv2.contourArea(x))
        
    #approx the contour a little
        epsilon = 0.0005*cv2.arcLength(cnt,True)
        approx= cv2.approxPolyDP(cnt,epsilon,True)
       
        
    #make convex hull around hand
        hull = cv2.convexHull(cnt)
        
     #define area of hull and area of hand
        areahull = cv2.contourArea(hull)
        areacnt = cv2.contourArea(cnt)
      
    #find the percentage of area not covered by hand in convex hull
        arearatio=((areahull-areacnt)/areacnt)*100
    
     #find the defects in convex hull with respect to hand
        hull = cv2.convexHull(approx, returnPoints=False)
        defects = cv2.convexityDefects(approx, hull)

        
        finger_count=detect_fingers(defects, approx, roi)
     
        #print corresponding gestures which are in their ranges
        font = cv2.FONT_HERSHEY_SIMPLEX
        result = display_finger_count(areacnt, arearatio, finger_count)
        cv2.putText(frame,result,(10,50), font, 2, (255,0,0), 3, cv2.LINE_AA)
            
    except:
        pass
    #show the window
    cv2.imshow('frame',frame)
        
    
    # Close the camera if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break
    
cv2.destroyAllWindows()
cap.release()    
