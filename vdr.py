import cv2
import numpy as np
import math
import imutils

def main():
	webcam = cv2.VideoCapture(0)
	button = cv2.imread("fb.png")
	button = imutils.resize(button, width=80)
	while(True):
		# Capture frame-by-frame
		ret,frame = webcam.read()
		''' conversion to hsv
		green = np.uint8([[[0,255,0 ]]])
		hsv_green = cv2.cvtColor(green,cv2.COLOR_BGR2HSV)
		'''
		h,w = placeButtons(frame,button)
		btnPos = (h,w)
		print(btnPos)

		skin = skin_detect(frame)
		cnt = findHandCnts(skin)
		shp = findSharpPoints(cnt)
		ftip = filterFingertips(shp)
		if( len(ftip) > 0 ):
			print(ftip)

		cv2.imshow("vid", frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	webcam.release()
	cv2.destroyAllWindows()

def placeButtons(frame, btn):
	f_height = frame.shape[0]
	f_width = frame.shape[1]
	t_height = btn.shape[0]
	t_width = btn.shape[1]
	fh = f_height/8
	fw = f_width/8
	height = fh - t_height/2
	width = fw - t_width/2
	frame[height:height+t_height, width:width+t_width] = btn
	return width, height

def skin_detect(frame):
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	lower_blue = np.array([0, 48, 80])
	upper_blue = np.array([20,255,255])
	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
	mask = cv2.erode(mask, kernel, iterations = 2)
	mask = cv2.dilate(mask, kernel, iterations = 2)
	# blur the mask to help remove noise, then apply the
	# mask to the frame
	mask = cv2.GaussianBlur(mask, (3, 3), 0)
	skin = cv2.bitwise_and(frame, frame, mask = mask)
	return skin

def findHandCnts(skin):
	gray = cv2.cvtColor(skin,cv2.COLOR_BGR2GRAY)
	blur = cv2.GaussianBlur(gray,(3,3),0)
	ret,thresh = cv2.threshold(blur,70,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
	image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
	cnt = max(contours, key = lambda x: cv2.contourArea(x))
	cv2.imshow('thres', thresh)
	return cnt

def findSharpPoints(handContour, curveLen = 75, curveAngleThresh = 50):
    if len(handContour) < 2*curveLen:
        return []
    extremePoints = []
    angleIndices = np.array([-2*curveLen,-curveLen,0])
    while angleIndices[2] < len(handContour):
        points = handContour[angleIndices] 
        ang = math.degrees(
                math.atan2(points[2][0][1]-points[1][0][1], points[2][0][0]-points[1][0][0]) -
                math.atan2(points[0][0][1]-points[1][0][1], points[0][0][0]-points[1][0][0])
              )
        while ang < 0:
            ang += 360
        while ang > 360:
            ang -= 360
        if ang < curveAngleThresh:
            extremePoints.append(tuple(points[1][0]))
        angleIndices += 1
    return extremePoints

def eDist(a,b):
    xd = a[0] - b[0]
    yd = a[1] - b[1]
    return math.sqrt(xd*xd + yd*yd)

def filterFingertips(sharpPoints, distThresh = 50):
    if len(sharpPoints) == 0:
        return []
    lastPoint = sharpPoints[0]
    centers = []
    clusteredPoints = [lastPoint]
    for p in sharpPoints[1:]:
        if eDist(lastPoint, p) > distThresh:
            centers.append(clusteredPoints[len(clusteredPoints)//2])
            clusteredPoints[:] = []
        clusteredPoints.append(p)
        lastPoint = p
    if len(clusteredPoints) > 0:
        centers.append(clusteredPoints[len(clusteredPoints)//2])
    return centers

def getHandCenter(handContour):
    handContourMoments = cv2.moments(handContour)
    return (int(handContourMoments['m10'] / handContourMoments['m00']),
            int(handContourMoments['m01'] / handContourMoments['m00']))

if __name__ == '__main__':
	main()
