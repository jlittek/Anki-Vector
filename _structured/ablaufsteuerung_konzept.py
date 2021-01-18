import threading
import sys
import time
import anki_vector
import numpy as np
from random import randint
from cv2 import cv2
from anki_vector.util import distance_mm, speed_mmps, degrees, Angle, Pose

def drive_for_search(robot):
	#Random hin und her fahren, drehen, ...
	#überprüfe zwischen jedem neuen motors.set_wheel_motors Aufruf, ob der Ball schon gefunden wurde, das reicht, da wenn search_ball() schon den Ball gefunden hat, eh schon in die Richtige richtung fährt
	#->spielfeld recht klein? Nur drehen?
	while True:
		while robot.ball_not_found:
			print("random drive")
			if randint(0,1)==0:
				robot.motors.set_wheel_motors(20,-20)
			else:
				robot.motors.set_wheel_motors(-20,20)
			time.sleep(randint(2,4))
			#if randint(0,1)==0:
				#fahren
				#robot.motors.set_wheel_motors(100,100)
			#else:
				#drehen random ob links oder rechts
				#if randint(0,1)==0:
					#robot.motors.set_wheel_motors(70,150)
				#else:
					#robot.motors.set_wheel_motors(150,70)
			#time.sleep(randint(1,2))

def getMiddleOfElement(img, bildRGB):
    contours, hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    found_cont=False
    for cnt in contours:
        area =cv2.contourArea(cnt)
        if(area>10):
            if(area>8000):
                #robot.behavior.set_head_angle(degrees(-10))
                #stelle um auf Abstandssensor um den zu sehen ob der Ball dran ist
                print("exit")
                sys.exit()
            #print("area:", area)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri,True)
            objCor = len(approx) #Anzahl der Ecken
            x, y, w, h = cv2.boundingRect(approx)
            if objCor > 7:
                cv2.circle(bildRGB, center=(int(x+w/2), int(y+h/2)), radius=int((h)/2), color=(0, 255, 0), thickness=3)
                return True, x+w/2, area
    return False, 640/2, None

def empty(a):
	pass

def change_direction(area, middle):
    #print(area)
    #Update desired drive direction 0<middle<640    
    if area<40:
        r=1
        l=1
    elif area>8000:
        r=0.5
        l=0.5
    else:
        l=-0.00006*area+1
        r=-0.00006*area+1
    if abs(320-middle)>250:
        l=l*0.6
        r=r*0.6
    if middle>320:
        l=1
    else:
        r=1
    robot.motors.set_wheel_motors(170*l,170*r)

def search_ball(robot):
	print("searching ball")
	#counter, how many camera images without finding ball
	frames=0
	while True:
		img=np.array(robot.camera.latest_image.raw_image)
		bildRGB = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
		bildBlur = cv2.GaussianBlur(bildRGB, (3,3), 1)
		bildHSV = cv2.cvtColor(bildBlur, cv2.COLOR_BGR2HSV)
		imgHSV = bildHSV
		lower = np.array([10, 66, 171])
		upper = np.array([47, 186, 255])
		#timwerte
		lower = np.array([0, 120, 168])
		upper = np.array([179, 255, 255])
		mask=cv2.inRange(imgHSV,lower,upper)
		imgContour=img.copy()
		success, middle, area = getMiddleOfElement(mask, bildRGB)
		cv2.namedWindow("Camera")
		cv2.imshow("Camera", bildRGB)
		cv2.namedWindow("Mask")
		cv2.imshow("Mask", mask)

		#Ball found?:
		if success==True:
			robot.ball_not_found=False
			change_direction(area, middle)
			frames=0
		else: # not found
			frames=frames+1
			if(frames>15):
				robot.ball_not_found=True

		if cv2.waitKey(1) & 0xFF == ord('q'):
			robot.disconnect()
			break

	#if ball unter Kontrolle -> drive_to_goal()

def drive_to_goal():
	print("drive_to_goal")
	#zum Tor fahren

def map(robot):
	map_height=160*3
	map_widht=100*3
	blank_image = np.zeros(shape=[map_height, map_widht, 3], dtype=np.uint8)
	cv2.circle(blank_image, center=(150,map_height-15 *3), radius=4, color=(0, 255, 0), thickness=20) #Start
	cv2.rectangle(blank_image,(40*3,0),(60*3,6),(255,0,0),12)
	while True:
		xcm=int(robot.pose.position.x/10)
		ycm=int(robot.pose.position.y/10)
		cv2.circle(blank_image, center=(150-ycm*3,map_height-(15*3+xcm*3)), radius=2, color=(0, 0, 255), thickness=2)
		if(robot.ball_not_found):
			cv2.putText(blank_image,"Ball not found ",(1,map_height-5),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,0,0))
		else:
			cv2.putText(blank_image,"Ball found ",(1,map_height-5),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,0))
		cv2.namedWindow("map")
		cv2.imshow("map", blank_image)
		if cv2.waitKey(1) & 0xFF==ord('q'):
			sys.exit()

def initialize():
	robot=anki_vector.Robot()
	robot.connect()
	robot.camera.init_camera_feed()
	robot.behavior.set_lift_height(0.0)
	robot.behavior.set_head_angle(degrees(0))
	robot.behavior.say_text("I'm ready!")
	robot.ball_not_found=False
	return robot

#starting robot
robot = initialize()
print("robot started")

#starting map
initmap = threading.Thread(target=map, args=[robot])
initmap.start()
print("Map started")

#starting searching Thread
drive_around_thread = threading.Thread(target=drive_for_search, args=[robot])
drive_around_thread.start()
print("drive_around started")

search_ball(robot)
#Ausführen und die ersten ca. 30 Bilder abwarten ob schon ein Ball erkannt, 
#wenn nicht, dann Ball suchen:
#ball_not_found=True
