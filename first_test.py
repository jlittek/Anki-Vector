
# Hallo
from cv2 import cv2
import numpy as np
import anki_vector
from anki_vector.util import distance_mm, speed_mmps, degrees

def empty(a):
    pass

#cap=cv2.VideoCapture(0)

#cv2.namedWindow("Trackbars")
#cv2.resizeWindow("Trackbars", 640,240)
#cv2.createTrackbar("H Min","Trackbars", 0, 179, empty)q
#cv2.createTrackbar("H Max","Trackbars", 179, 179, empty)
#cv2.createTrackbar("S Min","Trackbars", 0, 255, empty)
#cv2.createTrackbar("S Max","Trackbars", 255, 255, empty)
#cv2.createTrackbar("V Min","Trackbars", 0, 255, empty)
#cv2.createTrackbar("V Max","Trackbars", 255, 255, empty)
def searching():
    #random rumfahren -> muss in einem Thread sein
    while True:
        #hier noch random zahlen
        robot.motors.set_wheel_motors(100,100)
        time.sleep(1)



def getMiddleOfElement(img):
    contours, hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    found_cont=False
    for cnt in contours:
        area =cv2.contourArea(cnt)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02*peri,True)
        objCor = len(approx) #Anzahl der Ecken
        print(objCor)
        x, y, w, h = cv2.boundingRect(approx)
        #middle of contour
        #if area>1000: # erkennt den Ball in größerer Entfernung nicht, deshalb  nach Kreis suchen
        if objCor > 7:
            cv2.circle(img, center=(int(x+w/2), int(y+h/2)), radius=int((h)/2), color=(0, 255, 0), thickness=3)
            try:
                M = cv2.moments(cnt)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                #cv2.circle(imgContour, (cX, cY), 7, (255, 255, 255), -1)

                #print(cX)
                #Umgedreht, weil kamera gespiegelt -> anscheindn 640x360
                if (x+w/2)<300:
                    print("rechts")
                    change_handler(1)
                elif (x+w/2)<400:
                    print("mitte")
                    change_handler(2)
                else:
                    print("links")
                    change_handler(3) 
                return True
                
            except:
                pass
          
    print("not found")
    return False
        
            
def change_handler(direction):
    #Update desired drive direction
    #3-> rechts
    #2-> geradeaus
    #1-> links
    if(direction==2):
        robot.motors.set_wheel_motors(100,100)
    elif(direction==1):
        robot.motors.set_wheel_motors(75,100)
    elif(direction==3):
        robot.motors.set_wheel_motors(100,75)



robot=anki_vector.Robot()
robot.connect()
robot.camera.init_camera_feed()
robot.behavior.set_lift_height(0.0)
robot.behavior.set_head_angle(degrees(10))
print("Start reading")
print(robot.camera.latest_image.raw_image)

while True:
    img=np.array(robot.camera.latest_image.raw_image)
    imgHSV=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #Calibration:
    #h_min=cv2.getTrackbarPos("H Min","Trackbars")
    #h_max=cv2.getTrackbarPos("H Max","Trackbars")
    #s_min=cv2.getTrackbarPos("S Min","Trackbars")
    #s_max=cv2.getTrackbarPos("S Max","Trackbars")
    #v_min=cv2.getTrackbarPos("V Min","Trackbars")
    #v_max=cv2.getTrackbarPos("V Max","Trackbars")
    #Werte schon früher Calibriert für meinen Stift:
    h_min=0
    h_max=179
    s_min=150
    s_max=255
    v_min=154
    v_max=255
    #lower=np.array([h_min,s_min,v_min])
    #upper=np.array([h_max,s_max,v_max])
    lower = np.array([28, 124, 91]) 
    upper = np.array([130, 215, 255])

    mask=cv2.inRange(imgHSV,lower,upper)
    imgContour=img.copy()
    cv2.imshow("Camera", imgContour)
    cv2.imshow("Mask", mask)
    
    if getMiddleOfElement(mask)==False:
        robot.motors.set_wheel_motors(0,0)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
        robot.disconnect()

