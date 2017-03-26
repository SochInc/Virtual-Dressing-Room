import cv2
import imutils
import numpy as np
import ChangeClothes as cc
import random

import urllib.request
import pygame

def capture():
    global bytes
    stream = urllib.request.urlopen('http://10.42.0.205:8080/video')
    bytes = bytes()
    pygame.init()

    # cap = cv2.VideoCapture(0)
    images = cc.loadImages()
    thres = [130, 40, 75, 130]
    size = 180
    curClothId = 1
    th = thres[0]

    while True:
        bytes += stream.read(1024)
        a = bytes.find(b'\xff\xd8')
        b = bytes.find(b'\xff\xd9')
        if a != -1 and b != -1:
            jpg = bytes[a:b + 2]
            bytes = bytes[b + 2:]
            cam = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8), cv2.IMREAD_COLOR)


            # (ret, cam) = cap.read()
            # cam = cv2.flip(cam, 1, 0)
            t_shirt = images[curClothId]
            resized = imutils.resize(cam, width=800)
            gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
            circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)
            if circles is not None:
                circles = np.round(circles[0, :]).astype("int")
                for (x, y, r) in circles:
                    # only works if circle of radius 30 exists
                    if r > 30:
                        # draw circle and center of circle contour
                        cv2.circle(cam, (x, y), r, (0, 255, 0), 4)
                        cv2.rectangle(cam, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
                        # adjust size of tshirt according to radius of circle
                        size = r * 7
            if size > 350:
                size = 350
            elif size < 100:
                size = 100

            t_shirt = imutils.resize(t_shirt, width=size)

            f_height = cam.shape[0]
            f_width = cam.shape[1]
            t_height = t_shirt.shape[0]
            t_width = t_shirt.shape[1]
            height = f_height / 2 - t_height / 2
            width = f_width / 2 - t_width / 2
            rows, cols, channels = t_shirt.shape
            t_shirt_gray = cv2.cvtColor(t_shirt, cv2.COLOR_BGR2GRAY)
            ret, mask = cv2.threshold(t_shirt_gray, th, 255, cv2.THRESH_BINARY_INV)
            mask_inv = cv2.bitwise_not(mask)
            roi = cam[height:height + t_height, width:width + t_width]
            img_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)
            img_fg = cv2.bitwise_and(t_shirt, t_shirt, mask=mask)

            t_shirt = cv2.add(img_bg, img_fg)
            # cv2.imshow("tshirt", mask)

            cam[height:height + t_height, width:width + t_width] = t_shirt
            font = cv2.FONT_HERSHEY_PLAIN  # Creates a font
            x = 10  # position of text
            y = 20  # position of text

            cv2.putText(cam, "press 'n' key for next item, 'p' for previous and 'c' for snapshot", (x, y), font, .8, (255, 255, 255),
                        1)  # Draw the text
            cv2.namedWindow("Virtual Dressing Room", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("Virtual Dressing Room", int(cam.shape[1] * 1.4), int(cam.shape[0] * 1.4))
            cv2.imshow('Virtual Dressing Room', cam)
            key = cv2.waitKey(10)
            if key & 0xFF == ord('n'):
                if curClothId == len(images) - 1:
                    print("image out of bound")
                else:
                    curClothId += 1
                    th = thres[curClothId]
            if key & 0xFF == ord('c'):  # save on pressing 'y'
                rand = random.randint(1, 999999)

                cv2.imwrite('output/'+str(rand)+'.png', cam)

            if key & 0xFF == ord('p'):
                if curClothId == -1:
                    print("image out of bound")
                else:
                    curClothId -= 1

            if key == 27:
                break
    return
