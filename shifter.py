#!/usr/bin/env python

from RPi import GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)

matrix = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26]
for i, pin in enumerate(matrix):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

train8 = [
        GPIO.HIGH,
        GPIO.HIGH,
        GPIO.HIGH,
        GPIO.HIGH,
        GPIO.HIGH,
        GPIO.HIGH,
        GPIO.HIGH,
        GPIO.HIGH,

        GPIO.LOW,
        GPIO.LOW,
        GPIO.LOW,
        GPIO.LOW,
        GPIO.LOW,
        GPIO.LOW,
        GPIO.LOW,
        GPIO.LOW,
        ]

onoff = [
        GPIO.HIGH,
        GPIO.LOW,
        GPIO.HIGH,
        GPIO.LOW,
        GPIO.HIGH,
        GPIO.LOW,
        GPIO.HIGH,
        GPIO.LOW,

        GPIO.HIGH,
        GPIO.LOW,
        GPIO.HIGH,
        GPIO.LOW,
        GPIO.HIGH,
        GPIO.LOW,
        GPIO.HIGH,
        GPIO.LOW,
        ]

every = [GPIO.HIGH] * 16

one = [GPIO.HIGH] + [GPIO.LOW] * 15

tick = 0.1

srclk = matrix[0]
ser = matrix[1]
rclk = matrix[2]
srclr = matrix[3]

def reset():
    # reset
    GPIO.output(srclr, GPIO.LOW)
    sleep(0.1)
    GPIO.output(srclr, GPIO.HIGH)

def shift(bits):
    GPIO.output(srclk, GPIO.HIGH)
    for bit in bits:
        sleep(tick)
        GPIO.output(srclk, GPIO.LOW)
        GPIO.output(rclk, GPIO.LOW)
        GPIO.output(ser, bit)
        sleep(tick)
        GPIO.output(srclk, GPIO.HIGH)
        GPIO.output(rclk, GPIO.HIGH)

for bits in (one, every, onoff, train8):
    reset()
    shift(bits)
    sleep(2)

reset()
GPIO.cleanup()
