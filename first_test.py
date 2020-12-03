from cv2 import cv2
import numpy as np
import anki_vector
from anki_vector.util import distance_mm, speed_mmps

def empty(a):
    pass

cap=cv2.VideoCapture(0)

cv2.namedWindow("Trackbars")
cv2.resizeWindow("Trackbars", 640,240)
cv2.createTrackbar("H Min","Trackbars", 0, 179, empty)
cv2.createTrackbar("H Max","Trackbars", 179, 179, empty)
cv2.createTrackbar("S Min","Trackbars", 0, 255, empty)
cv2.createTrackbar("S Max","Trackbars", 255, 255, empty)
cv2.createTrackbar("V Min","Trackbars", 0, 255, empty)
cv2.createTrackbar("V Max","Trackbars", 255, 255, empty)

def getMiddleOfElement(img):
    contours, hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area =cv2.contourArea(cnt)
        #cv2.drawContours(imgContour,cnt,-1,(255,0,0),3)
        #middle of contour
        if area>1000:
            try:
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                cv2.circle(imgContour, (cX, cY), 7, (255, 255, 255), -1)

                #print(cX)
                #Umgedreht, weil kamera gespiegelt
                if cX<300:
                    print("rechts")
                elif cX<400:
                    print("mitte")
                    robot.behavior.drive_straight(distance_mm(200), speed_mmps(150))
                else:
                    print("links")
            except:
                pass

robot=anki_vector.Robot()
robot.connect()
robot.camera.init_camera_feed()
robot.behavior.set_lift_height(0.0)
print("Start reading")
while True:
    #success, img=cap.read()
    img=np.array(robot.camera.latest_image.raw_image)
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    h_min=cv2.getTrackbarPos("H Min","Trackbars")
    h_max=cv2.getTrackbarPos("H Max","Trackbars")
    s_min=cv2.getTrackbarPos("S Min","Trackbars")
    s_max=cv2.getTrackbarPos("S Max","Trackbars")
    v_min=cv2.getTrackbarPos("V Min","Trackbars")
    v_max=cv2.getTrackbarPos("V Max","Trackbars")
    #Werte schon früher Calibriert für meinen Stift:
    h_min=0
    h_max=179
    s_min=150
    s_max=255
    v_min=154
    v_max=255
    lower=np.array([h_min,s_min,v_min])
    upper=np.array([h_max,s_max,v_max])
    mask=cv2.inRange(imgHSV,lower,upper)
    imgContour=img.copy()

    getMiddleOfElement(mask)
    #cv2.circle(imgContour, (360, 150), 7, (0, 255, 0), -1)
    #cv2.imshow('image',imgContour)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        robot.disconnect()