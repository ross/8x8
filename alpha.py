#!/usr/bin/env python

from RPi import GPIO
from sys import argv
from time import sleep

from font8x8_basic import font8x8_basic

GPIO.setmode(GPIO.BOARD)

matrix = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26]
for i, pin in enumerate(matrix):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW if i < 8 else GPIO.HIGH)

ROW_ON = GPIO.HIGH
ROW_OFF = GPIO.LOW
ROW = [matrix[p] for p in range(8)]
COL_ON = GPIO.LOW
COL_OFF = GPIO.HIGH
COL = [matrix[p] for p in range(8, 16)]

FPS = 64
DELAY = 1.0 / FPS / 64  # 8x8 = 64

def render(ch, dur):
    point = ord(ch)
    data = font8x8_basic[point]
    for i in range(int(FPS * dur + 0.5)):
        for r in range(8):
            row_data = data[r]
            GPIO.output(ROW[r], ROW_ON)
            for c in range(8):
                if row_data & 1 << c:
                    GPIO.output(COL[c], COL_ON)
                sleep(DELAY)
                GPIO.output(COL[c], COL_OFF)
            GPIO.output(ROW[r], ROW_OFF)

try:
    msg = argv[1]
except IndexError:
    msg = 'Hello World!'

try:
    dur = float(argv[2])
except IndexError:
    dur = 0.5

for ch in msg:
    render(ch, dur)
