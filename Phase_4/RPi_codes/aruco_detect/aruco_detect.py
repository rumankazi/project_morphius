import numpy as np
import cv2
import cv2.aruco as aruco
import math

# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 4
rawCapture = PiRGBArray(camera, size=(640, 480))


camera_matrix = None
dist_coeff = None
#cap = cv2.VideoCapture(0)
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
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Capture frame-by-frame
    #ret, frame = cap.read()
    image = frame.array
    parameters = aruco.DetectorParameters_create()
    corners, ids, _ = aruco.detectMarkers(image, aruco_dict,parameters = parameters)
    rvec, tvec,_ = aruco.estimatePoseSingleMarkers(corners,0.1, cam, dist_coeff)
    
    aruco.drawDetectedMarkers(image,corners)
    if (np.any(ids!=None)):
        aruco.drawAxis(image,cam,dist_coeff,rvec[0],tvec[0],0.1)
        P=corners[0][0][0][0]-corners[0][0][1][0]
        dist=(F*W)/P
        #print("dist is ",dist)
        cv2.putText(image, "%.2f" % (dist),
		(image.shape[1] - 200, image.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX,
		1.0, (0, 255, 255), 3)
        print ('x = '+str(tvec[0][0][0]*100)+'y = '+str(tvec[0][0][1]*100)+'z = '+str(tvec[0][0][2]*100))
        
    # Display the resulting frame
    cv2.imshow('frame',image)
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
#cap.release()
#cv2.destroyAllWindows()
