from cv2 import cv2
import numpy as np  
import anki_vector
from anki_vector.util import distance_mm, speed_mmps, degrees


def empty(a):
    pass

robot=anki_vector.Robot()
robot.connect()
robot.camera.init_camera_feed()
robot.behavior.set_lift_height(0.0)
robot.behavior.set_head_angle(degrees(0))

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 600)
cv2.createTrackbar("Hue Min", "TrackBars", 10, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 47, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 66, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 186, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 171, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

while True:
    
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    img = np.array(robot.camera.latest_image.raw_image)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    imgBlur = cv2.GaussianBlur(img, (3,3), 1)
    imgHSV = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2HSV)

    print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(imgHSV, lower, upper)   

    # Alternative method to find the Ball: Approximation of the area with a Polygon.
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02*peri,True)
        objCor = len(approx) # Number of corners
        print(objCor)
        x, y, w, h = cv2.boundingRect(approx)

        if objCor > 6:
            cv2.circle(img, center=(int(x+w/2), int(y+h/2)), radius=int((h)/2), color=(0, 255, 0), thickness=3)
            
    cv2.imshow("Camera", img)
    cv2.imshow("Mask", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
