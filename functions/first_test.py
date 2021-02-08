from cv2 import cv2
import numpy as np
import anki_vector
from anki_vector.util import distance_mm, speed_mmps, degrees

def empty(a):
    pass

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
        print("area:", area)
        peri = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.02*peri,True)
        objCor = len(approx) #Anzahl der Ecken
        x, y, w, h = cv2.boundingRect(approx)
        if objCor > 7:
            cv2.circle(bildRGB, center=(int(x+w/2), int(y+h/2)), radius=int((h)/2), color=(0, 255, 0), thickness=3)
            return True, x+w/2, area
    print("not found")
    return False, 640/2, None
   
        
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

    bildRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    bildBlur = cv2.GaussianBlur(bildRGB, (3,3), 1)
    bildHSV = cv2.cvtColor(bildBlur, cv2.COLOR_BGR2HSV)
    imgHSV = bildHSV
    lower = np.array([10, 66, 171])
    upper = np.array([47, 186, 255])

    mask=cv2.inRange(imgHSV,lower,upper)
    imgContour=img.copy()


    success, middle, area = getMiddleOfElement(mask)

    cv2.imshow("Camera", bildRGB)
    cv2.imshow("Mask", mask)


    if success==True:
        if middle<250:
            print("links")
            change_handler(1)
        elif middle>350:
            print("rechts")
            change_handler(3)
        else:
            print("mitte")
            change_handler(1)
    else: # not found -> drehen
        robot.motors.set_wheel_motors(10,-10)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        robot.disconnect()
        break
