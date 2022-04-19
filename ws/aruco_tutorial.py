import cv2
import cv2.aruco as aruco
import numpy as np
import os

def findArucoMarkers(img, markerSize = 7, totalMarkers=50, draw=True):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray=cv2.threshold(gray,25,255,cv2.THRESH_BINARY)
    key = getattr(aruco, f'DICT_{markerSize}X{markerSize}_{totalMarkers}')
    arucoDict = aruco.Dictionary_get(key)
    arucoParam = aruco.DetectorParameters_create()
    bboxs, ids, rejected = aruco.detectMarkers(gray, arucoDict, parameters = arucoParam)
    print(ids)

url = "http://192.168.0.123:8080/shot.jpg"

cap = cv2.VideoCapture(0)
while True:
    print("hello")
    success, img = cap.read(url)
    findArucoMarkers(img)
    cv2.imshow('img',img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()