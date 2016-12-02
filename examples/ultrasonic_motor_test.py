#!/usr/bin/python
from Adafruit_MotorHAT import Adafruit_MotorHAT, Adafruit_DCMotor
import RPi.GPIO as GPIO

import time
import atexit

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

trigger = 18
echo = 24

GPIO.setup(trigger, GPIO.OUT)
GPIO.setup(echo, GPIO.IN)

GPIO.output(trigger, False)
time.sleep(2)

def distance(echo, trigger):
   GPIO.output(trigger, True)
   time.sleep(0.00001)
   GPIO.output(trigger, False)

   start = 0
   stop = 0
   
   while GPIO.input(echo) == 0:
      start = time.time()
      
   while GPIO.input(echo) == 1:
      stop = time.time()
   
   if stop != 0 and start != 0:
      elapsed = stop - start
      distance = elapsed * 33440
      distance = distance / 2
      return distance

"""while 0 == 0:
   distance(echo, trigger)
   time.sleep(0.5)"""

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


"""while (True):
	print "Forward! "
	m1.run(Adafruit_MotorHAT.FORWARD)
	m2.run(Adafruit_MotorHAT.FORWARD)
	m3.run(Adafruit_MotorHAT.FORWARD)
	m4.run(Adafruit_MotorHAT.FORWARD)

	print "\tSpeed up..."
	for i in range(255):
		m1.setSpeed(i)
		m2.setSpeed(i)
		m3.setSpeed(i)
		m4.setSpeed(i)
		time.sleep(0.01)

	print "\tSlow down..."
	for i in reversed(range(255)):
		m1.setSpeed(i)
		m2.setSpeed(i)
		m3.setSpeed(i)
		m4.setSpeed(i)
		time.sleep(0.01)

	print "Backward! "
	m1.run(Adafruit_MotorHAT.BACKWARD)
	m2.run(Adafruit_MotorHAT.BACKWARD)
	m3.run(Adafruit_MotorHAT.BACKWARD)
	m4.run(Adafruit_MotorHAT.BACKWARD)

	print "\tSpeed up..."
	for i in range(255):
		m1.setSpeed(i)
		m2.setSpeed(i)
		m3.setSpeed(i)
		m4.setSpeed(i)
		time.sleep(0.01)

	print "\tSlow down..."
	for i in reversed(range(255)):
		m1.setSpeed(i)
		m2.setSpeed(i)
		m3.setSpeed(i)
		m4.setSpeed(i)
		time.sleep(0.01)

	print "Release"
	m1.run(Adafruit_MotorHAT.RELEASE)
	m2.run(Adafruit_MotorHAT.RELEASE)
	m3.run(Adafruit_MotorHAT.RELEASE)
	m4.run(Adafruit_MotorHAT.RELEASE)
	time.sleep(1.0)"""

while(True):
   while distance(echo, trigger) > 10.0:
      m1.run(Adafruit_MotorHAT.FORWARD)
      m2.run(Adafruit_MotorHAT.FORWARD)
      m3.run(Adafruit_MotorHAT.FORWARD)
      m4.run(Adafruit_MotorHAT.FORWARD)
   else:
      m1.run(Adafruit_MotorHAT.RELEASE)
      m2.run(Adafruit_MotorHAT.RELEASE)
      m3.run(Adafruit_MotorHAT.RELEASE)
      m4.run(Adafruit_MotorHAT.RELEASE)
   time.sleep(0.5)
GPIO.cleanup()
