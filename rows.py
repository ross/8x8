#!/usr/bin/env python

from RPi import GPIO
from sys import stdin
from time import sleep

GPIO.setmode(GPIO.BOARD)

matrix = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26]
for i, pin in enumerate(matrix):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

row = [matrix[p] for p in range(8)]
col = [matrix[p] for p in range(8, 16)]
i = 0
while True:
    r = i % 8
    pin = row[r]
    print '{:02} {:02} {:02}'.format(i, r, pin)
    GPIO.output(pin, GPIO.HIGH)
    if stdin.readline() == 'x\n':
        break
    GPIO.output(pin, GPIO.LOW)
    i += 1

GPIO.cleanup()
