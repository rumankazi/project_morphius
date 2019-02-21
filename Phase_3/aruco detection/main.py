



import numpy as np
import cv2
import cv2.aruco as aruco
import math
camera_matrix = None
dist_coeff = None
cap = cv2.VideoCapture(0)
global aruco_dict
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
D = 24
W = 11
F = 300
def getCameraMatrix():
        global camera_matrix, dist_coeff
        with np.load('Camera.npz') as X:
                camera_matrix, dist_coeff, _, _ = [X[i] for i in ('mtx','dist','rvecs','tvecs')]
        return camera_matrix,dist_coeff

cam, dist_coeff = getCameraMatrix()
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(frame, aruco_dict,parameters = parameters)
    rvec, tvec, _= aruco.estimatePoseSingleMarkers(corners,0.28, cam, dist_coeff)
    aruco.drawDetectedMarkers(frame,corners)
    if (np.any(ids!=None)):
        aruco.drawAxis(frame,cam,dist_coeff,rvec[0],tvec[0],0.28)
        P=corners[0][0][0][0]-corners[0][0][1][0]
        dist=(F*W)/P
        #print("dist is ",dist)
        cv2.putText(frame, "%.2f" % (dist),
		(frame.shape[1] - 200, frame.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX,
		1.0, (0, 255, 255), 3)
    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
