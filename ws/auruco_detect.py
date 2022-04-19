import cv2
import sys
import argparse
import requests
import numpy as np
import imutils
import os
import matplotlib.pyplot as plt
import matplotlib as mpl



url = "http://192.168.1.7:8080/shot.jpg"

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

#url = "http://192.168.1.7:8080/shot.jpg"
#url = "http://25.83.15.127:8080/shot.jpg"
url = "http://192.168.137.214:8080/shot.jpg"



print("[INFO] starting video stream...")

# While loop to continuously fetching data from the Url
while True:
    img_resp = requests.get(url)
    print("hello")
    print(type(img_resp))
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8 )
    img = cv2.imdecode(img_arr, -1)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #h,l=gray.shape[:2]
    #print("h: ",h,"  l: ",l)
    #high, length = gray.shape[:2]
    #gray=cv2.threshold(gray,25,255,cv2.THRESH_BINARY)
    #print("high: ", high, "  length: ", length)
    #img = imutils.resize(gray, width=1000, height=1800)
    #cv2.imshow("Android_cam", img)
    arucoDict = cv2.aruco.Dictionary_get(ARUCO_DICT["DICT_7X7_250"])
    arucoParams = cv2.aruco.DetectorParameters_create()
    corners, ids, rejected = cv2.aruco.detectMarkers(img,arucoDict, parameters=arucoParams)


    frame_markers = cv2.aruco.drawDetectedMarkers(gray, corners, ids)
    print("ids:  ",ids)
    print(type(corners))
    print("----------------------")
    print(corners)
    #print(frame_markers)

    """    plt.figure()
    plt.imshow(frame_markers)
    for i in range(len(ids)):
	    c = corners[i][0]
	    plt.plot([c[:, 0].mean()], [c[:, 1].mean()], "o", label="id={0}".format(ids[i]))
    plt.legend()
    plt.show() """
    if len(corners) > 0:
    	# flatten the ArUco IDs list
        ids = ids.flatten()
    	# loop over the detected ArUCo corners
        for (markerCorner, markerID) in zip(corners, ids):
        	# extract the marker corners (which are always returned
        	# in top-left, top-right, bottom-right, and bottom-left
        	# order)
            corners = markerCorner.reshape((4, 2))
            (topLeft, topRight, bottomRight, bottomLeft) = corners
        	# convert each of the (x, y)-coordinate pairs to integers
            topRight = (int(topRight[0]), int(topRight[1]))
            bottomRight = (int(bottomRight[0]), int(bottomRight[1]))
            bottomLeft = (int(bottomLeft[0]), int(bottomLeft[1]))
            topLeft = (int(topLeft[0]), int(topLeft[1]))
        	# draw the bounding box of the ArUCo detection
            cv2.line(img, topLeft, topRight, (0, 255, 0), 2)
            cv2.line(img, topRight, bottomRight, (0, 255, 0), 2)
            cv2.line(img, bottomRight, bottomLeft, (0, 255, 0), 2)
            cv2.line(img, bottomLeft, topLeft, (0, 255, 0), 2)
        	# compute and draw the center (x, y)-coordinates of the
        	# ArUco marker
            cX = int((topLeft[0] + bottomRight[0]) / 2.0)
            cY = int((topLeft[1] + bottomRight[1]) / 2.0)
            cv2.circle(img, (cX, cY), 4, (0, 0, 255), -1)
            print("===========================calculated======")
        	# draw the ArUco marker ID on the img
            cv2.putText(img, str(markerID),
                    (topLeft[0], topLeft[1] - 15),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, (0, 255, 0), 2)
        	# show the output img
    cv2.imshow("img", img)
    key = cv2.waitKey(1) & 0xFF
    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

#cv2.destroyAllWindows()

