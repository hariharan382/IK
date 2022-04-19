import cv2
import cv2.aruco as aruco


import os
import requests
import numpy as np
import imutils
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

url = "http://192.168.0.123:8080/shot.jpg"

def findARuco(img, markersize=7, totalmarkers=50, draw=True):
    print(type(img))
    imggray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    key = getattr(aruco, f'DICT_{markersize}X{markersize}_{totalmarkers}')
    # print(key)
    arucoDict = aruco.Dictionary_get(ARUCO_DICT["DICT_7X7_50"])
    arucoParam = aruco.DetectorParameters_create()
    corners, ids, rejected = aruco.detectMarkers(imggray, arucoDict, parameters=arucoParam)
    if len(corners) > 0:
        print(ids)

        ids = ids.flatten()
        for (markerCorner, markerId) in zip(corners, ids):
            topLeft, topRight, bottonRight, bottonLeft = self.convert(corners)
            cv2.putText(frame, str(markerId), (topLeft[0] - 60, topLeft[1] - 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        (0, 255, 0), 2)
            print(ids)
def main():

	url = "http://192.168.0.123:8080/shot.jpg"
    img_resp = requests.get(url)
    img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)

    img = cv2.imdecode(img_arr, -1)

    img = imutils.resize(img, width=1000, height=1800)
    cap = cv2.VideoCapture(0)

    while True:
        #url = ""
        img_resp = requests.get(url)
        img_arr = np.array(bytearray(img_resp.content), dtype=np.uint8)

        img = cv2.imdecode(img_arr, -1)

        img = imutils.resize(img, width=1000, height=1800)
        ret, img=cap.read(img)
        findARuco(img)
        cv2.imshow("image",img)
        key = cv2.waitKey(1) & 0xFF
        # if the `q` key was pressed, break from the loop
        if key == ord("q"):
            break

if __name__ == "__main__":
    main()
