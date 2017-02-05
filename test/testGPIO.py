#!/usr/bin/env python

import os
import RPi.GPIO as GPIO
import time
import datetime
import sys

#Realy pin
FAN_PIN = 12

#set up pins
def GPIOsetup():
   # GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(FAN_PIN, GPIO.OUT)

GPIOsetup()
while True:
        GPIO.output(FAN_PIN, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(FAN_PIN, GPIO.LOW)
        time.sleep(1)