import threading
import time
import anki_vector
from random import randint
from anki_vector.util import distance_mm, speed_mmps, degrees

def drive_for_search():
	#Random hin und her fahren, drehen, ...
	#überprüfe zwischen jedem neuen motors.set_wheel_motors Aufruf, ob der Ball schon gefunden wurde, das reicht, da wenn search_ball() schon den Ball gefunden hat, eh schon in die Richtige richtung fährt
	global ball_not_found
	while ball_not_found:
		if randint(0,1)==0:
			#fahren
			robot.motors.set_wheel_motors(100,100)
		else:
			#drehen random ob links oder rechts
			if randint(0,1)==0:
				robot.motors.set_wheel_motors(50,100)
			else:
				robot.motors.set_wheel_motors(100,50)
		time.sleep(randint(1,2))

def search_ball():
	print("search_ball")
	#bisherige Implementierung von unserem Algorithmus um den Ball zu erkennen und auf ihn zuzufahren
	#Wenn Ball gefunden, drive_around beenden!
	#->
	#global ball_not_found
	#if ball found: ball_not_found=False
	#if ball nach einigen Bildern wieder verloren -> drive_and_search() + und hier beenden
	#if ball unter Kontrolle -> drive_to_goal()

def drive_to_goal():
	print("drive_to_goal")

	#zum Tor fahren
	#if Ball verloren -> drive_and_search()

def drive_and_search():
	print("drive_and_search")

	global ball_not_found
	ball_not_found=True
	drive_around_thread = threading.Thread(target=drive_for_search)
	search_ball_thread = threading.Thread(target=search_ball)
	drive_around_thread.start()
	search_ball_thread.start()

def initialize():
	robot=anki_vector.Robot()
	robot.connect()
	robot.camera.init_camera_feed()
	robot.behavior.set_lift_height(0.0)
	robot.behavior.set_head_angle(degrees(0))
	robot.behavior.say_text("I'm ready!")
	return robot

robot = initialize()
search_ball() 
#Ausführen und die ersten ca. 30 Bilder abwarten ob schon ein Ball erkannt, 
#wenn nicht, dann Ball suchen:
ball_not_found=True
drive_and_search()
