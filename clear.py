#!/usr/bin/env python

from RPi import GPIO
from sys import stdin
from time import sleep

GPIO.setmode(GPIO.BOARD)

matrix = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26]
for i, pin in enumerate(matrix):
    print 'Setting pin {} ({}) to output'.format(i, pin)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

GPIO.cleanup()
