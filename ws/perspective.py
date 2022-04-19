import math

import cv2
import sys
import argparse
import requests
import numpy as np
import imutils
import os
import matplotlib.pyplot as plt
import matplotlib as mpl
from operator import itemgetter
from glob import glob

#url = "http://192.168.1.7:8080/shot.jpg"
url = "http://192.168.137.214:8080/shot.jpg"

ARUCO_DICT = {
	"DICT_4X4_50": cv2.aruco.DICT_4X4_50,
	"DICT_4X4_100": cv2.aruco.DICT_4X4_100,
	"DICT_4X4_250": cv2.aruco.DICT_4X4_250,
	"DICT_4X4_1000": cv2.aruco.DICT_4X4_1000,
	"DICT_5X5_50": cv2.aruco.DICT_5X5_50,
	"DICT_5X5_100": cv2.aruco.DICT_5X5_100,
	"DICT_5X5_250": cv2.aruco.DICT_5X5_250,
	"DICT_5X5_1000": cv2.aruco.DICT_5X5_1000,
	"DICT_6X6_50": cv2.aruco.DICT_6X6_50,
	"DICT_6X6_100": cv2.aruco.DICT_6X6_100,
	"DICT_6X6_250": cv2.aruco.DICT_6X6_250,
	"DICT_6X6_1000": cv2.aruco.DICT_6X6_1000,
	"DICT_7X7_50": cv2.aruco.DICT_7X7_50,
	"DICT_7X7_100": cv2.aruco.DICT_7X7_100,
	"DICT_7X7_250": cv2.aruco.DICT_7X7_250,
	"DICT_7X7_1000": cv2.aruco.DICT_7X7_1000,
	"DICT_ARUCO_ORIGINAL": cv2.aruco.DICT_ARUCO_ORIGINAL,
	"DICT_APRILTAG_16h5": cv2.aruco.DICT_APRILTAG_16h5,
	"DICT_APRILTAG_25h9": cv2.aruco.DICT_APRILTAG_25h9,
	"DICT_APRILTAG_36h10": cv2.aruco.DICT_APRILTAG_36h10,
	"DICT_APRILTAG_36h11": cv2.aruco.DICT_APRILTAG_36h11
}

url = "http://192.168.137.214:8080/shot.jpg"
#url = "http://25.83.15.127:8080/shot.jpg"


print("[INFO] starting video stream...")

def dist(x1,y1,x2,y2):
    dist=math.sqrt((x2-x1)**2 +(y2-y1)**2)
    return dist



# While loop to continuously fetching data from the Url
while True:
    print("hello")
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8 )
    img = cv2.imdecode(img_arr, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_7X7_250"])
    arucoParams = cv2.aruco.DetectorParameters_create()
    corners, ids, rejected = cv2.aruco.detectMarkers(img,arucoDict, parameters=arucoParams)


    frame_markers = cv2.aruco.drawDetectedMarkers(gray, corners, ids)
    print("ids:  ",ids)
    """print("[[[[[[[[[[[[[[[[[[[[[[[")
    print(corners)
    print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\") """
    if len(corners) > 0:
        ids = ids.flatten()
        ids=ids.tolist()
        if 0 in ids:
            index_0=ids.index(0)
            markerSizeInCM = 0.05
            rvec, tvec, _ = cv2.aruco.estimatePoseSingleMarkers(corners[index_0][0], markerSizeInCM, mtx, dist)
            print(tvec)

            #print(corners)
            #print(type(corners))
            #print(np.shape(corners))
            #(topleft, topRight_0, bottomRight_0, bottomLeft_0) = corners[index_0]
            #bottomleft = corners[index_0][0][0]
            #dis=dist(corners[index_0][0][0][0],corners[index_0][0][0][1],corners[index_0][0][1][0],corners[index_0][0][1][1])
            #print("distance is : --" , dis)
            #print(topleft)
        if 1 in ids:
            index_1 = ids.index(1)
            #(topLeft_1, topRight_1, bottomright, bottomLeft_1) = corners
            bottomright = corners[index_1][0][1]
        if 2 in ids:
            index_2 = ids.index(2)
            #(topLeft_2, topright, bottomRight_2, bottomLeft_2) = corners
            topright = corners[index_2][0][2]
        if 3 in ids:
            index_3 = ids.index(3)
            #(topleft, topRight_3, bottomRight_3, bottomLeft_3) = corners
            topleft = corners[index_3][0][3]

        if set([0,1,2,3]).issubset(ids):
            print("inside the 4")
            # Coordinates that you want to Perspective Transform
            #pts1 = np.float32([[219, 209], [612, 8], [380, 493], [785, 271]])
            pts1 = np.float32([bottomleft, bottomright, topleft, topright])
            # Size of the Transformed Image
            pts2 = np.float32([[0, 0], [500, 0], [0, 500], [500, 500]])
            for val in pts1:
                cv2.circle(img, (val[0], val[1]), 5, (0, 255, 0), -1)
            M = cv2.getPerspectiveTransform(pts1, pts2)
            dst = cv2.warpPerspective(img, M, (500, 500))

            """cv2.circle(img, topleft, 4, (0, 0, 255), -1)
            cv2.circle(img, topright, 4, (0, 0, 255), -1)
            cv2.circle(img, bottomleft, 4, (0, 0, 255), -1)
            cv2.circle(img, bottomright, 4, (0, 0, 255), -1)"""
            cv2.imshow("img", dst)


        """for (markerCorner, markerID) in zip(corners, ids):
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))

            cv2.line(img, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(img, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(img, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(img, bottomLeft, topLeft, (0, 255, 0), 2)
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
            #print("===========================calculated======")
        	# draw the ArUco marker ID on the img
            cv2.putText(img, str(markerID),
                    (topLeft[0], topLeft[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        	# show the output img"""
    #cv2.imshow("img", img)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

#cv2.destroyAllWindows()

