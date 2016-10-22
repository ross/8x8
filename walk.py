#!/usr/bin/env python

from RPi import GPIO
from sys import argv
from time import sleep

GPIO.setmode(GPIO.BOARD)

matrix = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26]
for i, pin in enumerate(matrix):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW if i < 8 else GPIO.HIGH)

ROW_ON = GPIO.HIGH
ROW_OFF = GPIO.LOW
COL_ON = GPIO.LOW
COL_OFF = GPIO.HIGH
row = [matrix[p] for p in range(8)]
col = [matrix[p] for p in range(8, 16)]

try:
    delay = float(argv[1])
except ValueError:
    delay = 0.05

# right to left, top to bottom
for i in range(8):
    GPIO.output(row[i], ROW_ON)
    for j in range(8):
        GPIO.output(col[j], COL_ON)
        sleep(delay)
        GPIO.output(col[j], COL_OFF)
    GPIO.output(row[i], ROW_OFF)

# back and forth
for i in range(8):
    GPIO.output(row[i], ROW_ON)
    cols = range(8) if i % 2 == 0 else range(7, 0, -1)
    for j in cols:
        GPIO.output(col[j], COL_ON)
        sleep(delay)
        GPIO.output(col[j], COL_OFF)
    GPIO.output(row[i], ROW_OFF)

# up and down
for i in range(8):
    GPIO.output(col[i], COL_ON)
    cols = range(8) if i % 2 == 0 else range(7, 0, -1)
    for j in cols:
        GPIO.output(row[j], ROW_ON)
        sleep(delay)
        GPIO.output(row[j], ROW_OFF)
    GPIO.output(col[i], COL_OFF)

GPIO.cleanup()
