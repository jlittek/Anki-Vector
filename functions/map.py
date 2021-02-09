from cv2 import cv2
import numpy as np
import anki_vector
import sys

def map(robot):
    # Map to track the robot's path during the game:
	map_height = 160*3
	map_widht = 100*3
	blank_image = np.zeros(shape=[map_height, map_widht, 3], dtype=np.uint8)
	cv2.circle(blank_image, center=(150,map_height-15 *3), radius=4, color=(0, 255, 0), thickness=20) #Start
	cv2.rectangle(blank_image,(40*3,0),(60*3,6),(255,0,0),12)
	while True:
		xcm = int(robot.pose.position.x/10)
		ycm = int(robot.pose.position.y/10)
		cv2.circle(blank_image, center=(150-ycm*3,map_height-(15*3+xcm*3)), radius=2, color=(0, 0, 255), thickness=2)
		if(robot.ball_not_found):
			cv2.putText(blank_image,"Ball not found ",(1,map_height-5),cv2.FONT_HERSHEY_SIMPLEX,0.4,(255,0,0))
		else:
			cv2.putText(blank_image,"Ball found ",(1,map_height-5),cv2.FONT_HERSHEY_SIMPLEX,0.4,(0,255,0))
		cv2.namedWindow("map")
		cv2.imshow("map", blank_image)
		if cv2.waitKey(1) & 0xFF==ord('q'):
			sys.exit()