import cv2
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
cv2.createTrackbar("Hue Min", "TrackBars", 0, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 113, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 99, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 108, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 92, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 180, 255, empty)

while True:
    
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    bild = np.array(robot.camera.latest_image.raw_image)
    bildRGB = cv2.cvtColor(bild, cv2.COLOR_RGB2BGR)
    bildBlur = cv2.GaussianBlur(bildRGB, (kernelsize,kernelsize), 1)
    bildHSV = cv2.cvtColor(bildBlur, cv2.COLOR_BGR2HSV)

    print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(bildHSV, lower, upper)   

    contours, hierarchy=cv2.findContours(mask,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02*peri,True)
        objCor = len(approx) #Anzahl der Ecken
        print(objCor)
        x, y, w, h = cv2.boundingRect(approx)

        if objCor > 6:
            cv2.circle(bildRGB, center=(int(x+w/2), int(y+h/2)), radius=int((h)/2), color=(0, 255, 0), thickness=3)
            
    cv2.imshow("Bild RGB", bildRGB)
    cv2.imshow("Maske", mask)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break