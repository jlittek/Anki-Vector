import threading
import sys
import time
import anki_vector
import numpy as np
from random import randint
from cv2 import cv2
from anki_vector.util import distance_mm, speed_mmps, degrees, Angle, Pose
from anki_vector.events import Events
import math

def handle_object_observed(robot, event_type, event):
    # This will be called whenever an EvtObjectObserved is dispatched -
    # whenever an Object comes into view.
    for obj in robot.world.visible_custom_objects:
        if obj.custom_type == anki_vector.objects.CustomObjectTypes.CustomType00:
            robot.goal_pose = obj.pose

def drive_for_search(robot):
    #überprüfe zwischen jedem neuen motors.set_wheel_motors Aufruf, ob der Ball schon gefunden wurde, das reicht, da wenn search_ball() schon den Ball gefunden hat, eh schon in die Richtige richtung fährt
    while True:
        while robot.ball_not_found:
            robot.motors.set_wheel_motors(-15,15)
            time.sleep(randint(2,4))

def getMiddleOfElement_area(img, bildRGB):
	contours, hierarchy=cv2.findContours(img,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	found_cont=False
	for cnt in contours:
		area =cv2.contourArea(cnt)
		if area>20:
			if area>3500:
				print("BALLL")
				return True, 640/2, area, True #Ball gefunden und nah dran
			print(area)
			try:
				M = cv2.moments(cnt)
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				cv2.circle(bildRGB, (cX, cY), 7, (255, 255, 255), -1)
				return True, cX, area, False #Ball gefunden, aber noch nicht nah genug
			except:
				pass	
	return False, 640/2, None, False #Ball nicht gefunden

def change_direction(area, middle):
    d = middle-320
    a=math.sqrt(50/area)/2
    robot.motors.set_wheel_motors(80*d/320, -80*d/320)
    robot.motors.set_wheel_motors(60*a+60,60*a+60)
 
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
        lower = np.array([0, 116, 148])
        upper = np.array([30, 229, 255])
        mask=cv2.inRange(imgHSV,lower,upper)
        imgContour=img.copy()
        success, middle, area, goal = getMiddleOfElement_area(mask, bildRGB)
        cv2.namedWindow("Camera")
        cv2.imshow("Camera", bildRGB)
        cv2.namedWindow("Mask")
        cv2.imshow("Mask", mask)
        #Ball found?:
        if success==True:
            robot.ball_not_found=False
            frames=0
            if robot.drivegoal==False:
                robot.behavior.set_lift_height(1.0)
            if goal==True and robot.drivegoal==False:
                robot.behavior.set_lift_height(0.2)
                robot.motors.stop_all_motors()
                print("drive_to_goal")
                robot.behavior.drive_straight(distance_mm(-150), speed_mmps(100))
                print("I got the ball from my opponent.")
                x = robot.goal_pose.position.x-robot.pose.position.x
                y = robot.pose.position.y
                distance_to_goal = math.sqrt(x*x+y*y)
                angle_to_goal = np.rad2deg(np.arcsin(x/distance_to_goal))
                print("alpha:", angle_to_goal)
                if y > 0:
                    robot.behavior.turn_in_place(degrees(-0.8*(90-angle_to_goal)), is_absolute=True)
                else:
                    robot.behavior.turn_in_place(degrees(0.8*(90-angle_to_goal)), is_absolute=True)
                robot.motors.set_wheel_motors(100,100)
                robot.drivegoal=True
                #Thread, damit weiter gescannt werde kann, ob Ball auf dem Weg zum Tor verloren gegangen ist
                drive_goal = threading.Thread(target=drive_to_goal, args=[robot, x, y])
                drive_goal.start()
            elif robot.drivegoal==False:
                change_direction(area, middle)
        else: # not found
            frames=frames+1
        if(frames>1):
            robot.drivegoal=False
            robot.ball_not_found=True
        if cv2.waitKey(1) & 0xFF == ord('q'):
            robot.disconnect()
            sys.exit()
            return False

def drive_to_goal(robot, x, y):
    while robot.drivegoal:
        x = robot.goal_pose.position.x-robot.pose.position.x
        y = robot.pose.position.y
        if x<50 and abs(y)<50: 
            print("Goal")
            robot.drivegoal=False
            robot.disconnect()
            sys.exit()
            break
    robot.motors.stop_all_motors()
    return
  
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
	robot.goal_pose = Pose(x=(160-15)*10, y=0, z=0, angle_z=anki_vector.util.Angle(degrees=0))
	robot.events.subscribe(handle_object_observed, Events.object_observed)
	robot.enable_custom_object_detection=True
	robot.world.define_custom_wall(anki_vector.objects.CustomObjectTypes.CustomType00, anki_vector.objects.CustomObjectMarkers.Triangles5, width_mm=200.0, height_mm=300.0, marker_width_mm=170.0, marker_height_mm=170.0)
	robot.behavior.say_text("I'm ready!")
	robot.ball_not_found=True
	robot.drivegoal=False
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
