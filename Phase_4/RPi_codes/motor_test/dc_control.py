import RPi.GPIO as GPIO
from time import sleep

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


    pwm1.start(100)
    pwm2.start(100)
    
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

try:
    setup()
except KeyboardInterrupt:
    print('Int received')
except:
    print('some err')
finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()

    


    
