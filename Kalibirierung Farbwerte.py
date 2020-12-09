import cv2
import numpy as np  #?
video = cv2.VideoCapture(0)
bild = cv2.imread("C:/Users/JonasLittek/Pictures/Screenshots/Screenshot (297).png")
bildBlur = cv2.GaussianBlur(bild, (7,7), 1)
bildHSV = cv2.cvtColor(bildBlur, cv2.COLOR_BGR2HSV)
def empty(a):
    pass

cv2.namedWindow("TrackBars")
cv2.resizeWindow("TrackBars", 640, 240)
cv2.createTrackbar("Hue Min", "TrackBars", 13, 179, empty)
cv2.createTrackbar("Hue Max", "TrackBars", 17, 179, empty)
cv2.createTrackbar("Sat Min", "TrackBars", 128, 255, empty)
cv2.createTrackbar("Sat Max", "TrackBars", 255, 255, empty)
cv2.createTrackbar("Val Min", "TrackBars", 158, 255, empty)
cv2.createTrackbar("Val Max", "TrackBars", 255, 255, empty)

while True:
    h_min = cv2.getTrackbarPos("Hue Min", "TrackBars")
    h_max = cv2.getTrackbarPos("Hue Max", "TrackBars")
    s_min = cv2.getTrackbarPos("Sat Min", "TrackBars")
    s_max = cv2.getTrackbarPos("Sat Max", "TrackBars")
    v_min = cv2.getTrackbarPos("Val Min", "TrackBars")
    v_max = cv2.getTrackbarPos("Val Max", "TrackBars")

    print(h_min, h_max, s_min, s_max, v_min, v_max)
    lower = np.array([h_min, s_min, v_min])
    upper = np.array([h_max, s_max, v_max])
    mask = cv2.inRange(bildHSV, lower, upper)   #?

    cv2.imshow("Original", bild)
  
    cv2.imshow("HSV", mask)
  
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break