
# HAND GESTURE RECOGNITION USING LAPTOP WEB CAMERA

In this project, I have detected hand gestures using convexHull defects and displayed them.
I have used calibration and thresholding using hsv values for hand segmentation and then found contours to find the defects using convexHull() function.

Additionally I have tried to control keyboard and mouse actions using pyautogui library in python and I tried to display the gestures in video by using text.


To execute the code follow these steps

Install Visual Studio code editor or use jupyter notebook to execute the python file named exper.py

The desired output can be obtained by executing and running exper.py file

Make sure to install python packages cv2, numpy, math, pyautogui
If not available use below command

pip install package_name example: pip install cv2

After successfull installation of all packages, run the code exper.py file

The program opens the web camera, displays a bounding box, place your hand in bounding box and show the finger count 1, 2, 3, 4, 5. It displays the count accordingly in the video and also you can see "Best of luck" and "ok" depending on the area covered by hand. If not hand is placed in bounding box, it prompts to place the hand in box.

To exit press q

The experiments done for different segmentation methods are present in files listed below

CANNY EDGE DETECTION experiment in canny.py file

BACKGROUND SEGMENTATION in pg2.py file

CALIBRATION AND THRESHOLDING in thresh1.py and thresh2.py files

