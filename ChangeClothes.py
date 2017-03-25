import os
import cv2
def loadImages():
    folder = "tshirt"
    images = []
    thres = [40, 75, 130, 130];
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images