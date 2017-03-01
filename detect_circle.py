import cv2
import imutils
import numpy as np

cap = cv2.VideoCapture(0)
size = 180

while True:
	(ret, cam) = cap.read()
	cam = cv2.flip(cam, 1, 0)

	t_shirt = cv2.imread("t_shirt3.jpg", -1)
	resized = imutils.resize(cam, width=800)
	gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
	circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
	if circles is not None:
		circles = np.round(circles[0, :]).astype("int")
		for (x, y, r) in circles:
			# only works if circle of radius 30 exists
			if r>30:
				# draw circle and center of circle contour
				cv2.circle(cam, (x, y), r, (0, 255, 0), 4)
				cv2.rectangle(cam, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
				# adjust size of tshirt according to radius of circle
				size = r*4
	if size>350:
		size = 350
	elif size<100:
		size = 100

	t_shirt = imutils.resize(t_shirt, width=size)

	f_height = cam.shape[0]
	f_width = cam.shape[1]
	t_height = t_shirt.shape[0]
	t_width = t_shirt.shape[1]
	height = f_height/2 - t_height/2
	width = f_width/2 - t_width/2

	rows,cols,channels = t_shirt.shape
	t_shirt_gray = cv2.cvtColor(t_shirt,cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(t_shirt_gray, 200, 255, cv2.THRESH_BINARY_INV)
	mask_inv = cv2.bitwise_not(mask)
	roi = cam[height:height+t_height, width:width+t_width]
	img_bg = cv2.bitwise_and(roi,roi,mask = mask_inv)
	img_fg = cv2.bitwise_and(t_shirt,t_shirt,mask = mask)

	t_shirt = cv2.add(img_bg,img_fg)
	cv2.imshow("tshirt", mask)

	cam[height:height+t_height, width:width+t_width] = t_shirt

	cv2.imshow('Image', cam)
	k = cv2.waitKey(10)
	if k == 27:
		break