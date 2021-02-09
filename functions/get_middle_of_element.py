import cv2

def getMiddleOfElement_area(img, bildRGB):
    # analyze the "white spots" found in serach_ball
	contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	found_cont = False
	for cnt in contours:
		area = cv2.contourArea(cnt)
		if area > 20:
			if area > 3500:
				print("BALLL")
				return True, 640/2, area, True # Ball found and close to it
			print(area)
			try:
                # Compute the middle of the area identified as the ball:
				M = cv2.moments(cnt)
				cX = int(M["m10"] / M["m00"])
				cY = int(M["m01"] / M["m00"])
				cv2.circle(bildRGB, (cX, cY), 7, (255, 255, 255), -1)
				return True, cX, area, False # Ball found, but not close enough
			except:
				pass	
	return False, 640/2, None, False # Ball not found


