import RPi.GPIO as GPIO
from time import sleep
import numpy as np
import cv2
import cv2.aruco as aruco
import math
import RPi.GPIO as GPIO
import time

#GPIO.setmode(GPIO.BOARD)
GPIO.setmode(GPIO.BCM)

GPIO.setup(18, GPIO.OUT)

p = GPIO.PWM(18, 50)

p.start(2.5)
# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 24
rawCapture = PiRGBArray(camera, size=(640, 480))


camera_matrix = None
dist_coeff = None
#cap = cv2.VideoCapture(0)
global aruco_dict
aruco_dict = aruco.Dictionary_get(aruco.DICT_5X5_250)
D = 24
W = 11
F = 300
###############################################
Motor1A=23
Motor1B=24
Motor1E=25

Motor2A=27
Motor2B=17
Motor2E=22
GPIO.setmode(GPIO.BCM)
GPIO.setup(Motor1A,GPIO.OUT)
GPIO.setup(Motor1B,GPIO.OUT)
GPIO.setup(Motor1E,GPIO.OUT)

GPIO.setup(Motor2A,GPIO.OUT)
GPIO.setup(Motor2B,GPIO.OUT)
GPIO.setup(Motor2E,GPIO.OUT)
pwm1 = GPIO.PWM(25,100)
pwm2 = GPIO.PWM(22,100)

def setup():
    pwm1.start(50)
    pwm2.start(50)
    
    GPIO.output(Motor1A,GPIO.HIGH) 
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

    sleep(1)
    
    GPIO.output(Motor1A,GPIO.LOW) 
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.LOW)

    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)

def destroy():
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
def forward():
    GPIO.output(Motor1A,GPIO.HIGH) 
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH) 
    
def back():
    GPIO.output(Motor1A,GPIO.LOW) 
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)   
       
def turn_right():
    GPIO.output(Motor1A,GPIO.LOW) 
    GPIO.output(Motor1B,GPIO.HIGH)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.HIGH)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.HIGH)

def turn_left():
    GPIO.output(Motor1A,GPIO.HIGH) 
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.HIGH)

    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.HIGH)
    GPIO.output(Motor2E,GPIO.HIGH)

def stop():
    GPIO.output(Motor1A,GPIO.LOW) 
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor1E,GPIO.LOW)

    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor2E,GPIO.LOW)
#setup()
#destroy()

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
    rvec, tvec,_ = aruco.estimatePoseSingleMarkers(corners,0.28, cam, dist_coeff)
    
    aruco.drawDetectedMarkers(image,corners)
    if (np.any(ids!=None)):
        aruco.drawAxis(image,cam,dist_coeff,rvec[0],tvec[0],0.28)
        P=corners[0][0][0][0]-corners[0][0][1][0]
        dist=(F*W)/P
        #print("dist is ",dist)
        cv2.putText(image, "%.2f" % (dist),
		(image.shape[1] - 200, image.shape[0] - 30), cv2.FONT_HERSHEY_SIMPLEX,
		1.0, (0, 255, 255), 3)
        print ('x = '+str(tvec[0][0][0]*100)+'y = '+str(tvec[0][0][1]*100)+'z = '+str(tvec[0][0][2]*100))
        y_value = tvec[0][0][1]*100
        x_value = tvec[0][0][0]*100
        z_value = tvec[0][0][2]*100
        #pwm1.start(50)
        #pwm2.start(50)
        #forward()
        if z_value>250:
            pwm1.start(20)
            pwm2.start(20)
            forward()
            
        elif z_value < 150:
            pwm1.start(15)
            pwm2.start(15)
            back()
            print("back")
    #if y_value>0:


                
        else:
            if y_value < 45 or  y_value > -45:
                y_value = 45 - y_value
                p.ChangeDutyCycle(2.7+(y_value*0.05))
                print("arm")
            if x_value > 10 and x_value < 55:
                pwm1.start(1.8181*x_value)
                pwm2.start(1.181*x_value)
                print("lef\n")
                turn_left()
            elif x_value < -10 and x_value > -55:
                pwm1.start(-1.8181*x_value)
                pwm2.start(-1.8181*x_value)
                turn_right()
                print("right\n")
            else:
                stop()

        #else:
        #    stop()
        
    # Display the resulting frame
    cv2.imshow('frame',image)
    rawCapture.truncate(0)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        p.stop()
        GPIO.cleanup()
        break

# When everything done, release the capture
#cap.release()
#cv2.destroyAllWindows()



##try:
##    setup()
##except KeyboardInterrupt:
##    print('Int received')
##except:
##    print('some err')
##finally:
##    pwm1.stop()
##    pwm2.stop()
##    GPIO.cleanup()

    


    
