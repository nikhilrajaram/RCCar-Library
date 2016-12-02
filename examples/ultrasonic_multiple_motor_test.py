#!/usr/bin/python
import sys
sys.path.append('/home/pi/RCCar-Library')
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import RPi.GPIO as GPIO

import time
import atexit

GPIO.setwarnings(False)
# nulls warning outputs we don't need
GPIO.setmode(GPIO.BCM)
# sets the GPIO board to the BCM mode (read up on BCM vs BOARD if interested but not necessary)

t1 = 21
t2 = 20
t3 = 12
# t stands for trigger, 1 and 2 correspond to the respective ultrasonic sensors
# the trigger is a GPIO out from the RPi, it sends a short impulse to the ultrasonic sensor to initialize it
e1 = 24
e2 = 22
e3 = 18
# e stands for echo, 1 and 2 correspond to the respective ultrasonic sensors
# the echo is a GPIO in to the RPi, the sensors send out square waves that we can use to calculate distance

GPIO.setup(t1, GPIO.OUT)
GPIO.setup(e1, GPIO.IN)
GPIO.setup(t2, GPIO.OUT)
GPIO.setup(e2, GPIO.IN)
GPIO.setup(t3, GPIO.OUT)
GPIO.setup(e3, GPIO.IN)
# this block of code sets up the pins as inputs or outputs

GPIO.output(t1, False)
GPIO.output(t2, False)
GPIO.output(t3, False)
time.sleep(0.5)
# required to sleep and wake the sensors

def distance(echo, trigger):
   GPIO.output(trigger, True)
   time.sleep(0.00001)
   GPIO.output(trigger, False)
   # initializes the sensors

   start = 0
   stop = 0
   
   while GPIO.input(echo) == 0:
      start = time.time()
      # loops for when echo terminal receives no sonic input
      
   while GPIO.input(echo) == 1:
      stop = time.time()
      # loops for when echo terminal receives a sonic input
   
   if stop != 0 and start != 0:
      elapsed = stop - start # measures the time between the emission of a wave and a reception of a reflected wave
      distance = elapsed * 33440 # multiplies this time by the speed of sound at approx 5280 ft in cm/s 
      distance = distance / 2 # halves the measured distance since the wave traveled double the actual distance
      return distance

# create a default object, no changes to I2C address or frequency
mh = Adafruit_MotorHAT(addr=0x60)

# recommended for auto-disabling motors on shutdown!
def turnOffMotors():
	mh.getMotor(1).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(2).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(3).run(Adafruit_MotorHAT.RELEASE)
	mh.getMotor(4).run(Adafruit_MotorHAT.RELEASE)

atexit.register(turnOffMotors)

################################# DC motor test!
m1 = mh.getMotor(1)
m2 = mh.getMotor(2)
m3 = mh.getMotor(3)
m4 = mh.getMotor(4)

# set the speed to start, from 0 (off) to 255 (max speed)
m1.setSpeed(150)
m2.setSpeed(150)
m3.setSpeed(150)
m4.setSpeed(150)

m1.run(Adafruit_MotorHAT.FORWARD);
m2.run(Adafruit_MotorHAT.FORWARD);
m3.run(Adafruit_MotorHAT.FORWARD);
m4.run(Adafruit_MotorHAT.FORWARD);
# turn on motor
m1.run(Adafruit_MotorHAT.RELEASE);
m2.run(Adafruit_MotorHAT.RELEASE);
m3.run(Adafruit_MotorHAT.RELEASE);
m4.run(Adafruit_MotorHAT.RELEASE);

while(True):
   print "Front: " + str(distance(e2, t2))
   print "Left: " + str(distance(e1, t1))
   print "Right: " + str(distance(e3, t3))
   if distance(e1, t1) > 10.0 and distance(e3, t3) > 10.0 and distance(e2, t2) > 10.0:
      m1.run(Adafruit_MotorHAT.FORWARD)
      m2.run(Adafruit_MotorHAT.FORWARD)
      m3.run(Adafruit_MotorHAT.FORWARD)
      m4.run(Adafruit_MotorHAT.FORWARD)
      m1.setSpeed(100)
      m2.setSpeed(100)
      m3.setSpeed(100)
      m4.setSpeed(100)
   elif distance(e1, t1) < 10.0 and distance(e2, t2) > 10.0:
      m1.run(Adafruit_MotorHAT.BACKWARD)
      m2.run(Adafruit_MotorHAT.BACKWARD)
      m1.setSpeed(0)
      m2.setSpeed(0)
      m3.run(Adafruit_MotorHAT.FORWARD)
      m4.run(Adafruit_MotorHAT.FORWARD)
      m3.setSpeed(255)
      m4.setSpeed(255)
   elif distance(e3, t3) < 10.0 and distance(e1, t1) > 10.0:
      m1.run(Adafruit_MotorHAT.FORWARD)
      m2.run(Adafruit_MotorHAT.FORWARD)
      m1.setSpeed(255)
      m2.setSpeed(255)
      m3.run(Adafruit_MotorHAT.BACKWARD)
      m4.run(Adafruit_MotorHAT.BACKWARD)
      m3.setSpeed(0)
      m4.setSpeed(0)
   elif distance(e2, t2) < 10.0:
      m1.run(Adafruit_MotorHAT.BACKWARD)
      m2.run(Adafruit_MotorHAT.BACKWARD)
      m3.run(Adafruit_MotorHAT.BACKWARD)
      m4.run(Adafruit_MotorHAT.BACKWARD)
   time.sleep(0.4)
   # delays the sensor a bit so Python doesn't screw up timing (it isn't that timely of a language)

GPIO.cleanup() # required after any code involving setting up GPIO pins
