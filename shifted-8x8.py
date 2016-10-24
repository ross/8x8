#!/usr/bin/env python

from RPi import GPIO
from threading import Thread
from time import sleep

from font8x8_basic import font8x8_basic


GPIO.setmode(GPIO.BOARD)

matrix = [3, 5, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 21, 22, 23, 24, 26]
for i, pin in enumerate(matrix):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


class Display(Thread):

    def __init__(self, latch, col_srclk, col_ser, row_srclk, row_ser,
                 refresh_rate=32):
        super(Display, self).__init__(name='display')

        self.latch = latch
        self.col_srclk = col_srclk
        self.col_ser = col_ser
        self.row_srclk = row_srclk
        self.row_ser = row_ser
        self.refresh_rate = refresh_rate

        self._com_delay = 1 / 9600

        self._data = [0x00] * 8
        self.reset()

    def set(self, data):
        self._data = data

    def run(self):
        self._running = True

        while self._running:
            self._refresh()

    def stop(self):
        self._running = False
        self.join()
        display.reset()

    def reset(self):
        GPIO.output(self.latch, GPIO.LOW)

        for i in range(8):
            GPIO.output(self.col_srclk, GPIO.LOW)
            GPIO.output(self.row_srclk, GPIO.LOW)
            GPIO.output(self.col_ser, GPIO.LOW)
            GPIO.output(self.row_ser, GPIO.LOW)
            sleep(self._com_delay)
            GPIO.output(self.col_srclk, GPIO.HIGH)
            GPIO.output(self.row_srclk, GPIO.HIGH)

        GPIO.output(self.latch, GPIO.HIGH)

    def test(self):
        GPIO.output(self.latch, GPIO.LOW)

        # turn all rows on
        GPIO.output(self.row_ser, GPIO.HIGH)
        for r in range(8):
            GPIO.output(self.row_srclk, GPIO.LOW)
            sleep(self._com_delay)
            GPIO.output(self.row_srclk, GPIO.HIGH)

        # turn all cols on
        GPIO.output(self.col_ser, GPIO.HIGH)
        for c in range(8):
            GPIO.output(self.col_srclk, GPIO.LOW)
            sleep(self._com_delay)
            GPIO.output(self.col_srclk, GPIO.HIGH)

        GPIO.output(self.latch, GPIO.HIGH)

    def _refresh(self):
        delay = 1 / self.refresh_rate / 64

        # col starts out high
        GPIO.output(self.col_ser, GPIO.HIGH)
        for c in range(8):
            GPIO.output(self.latch, GPIO.LOW)

            GPIO.output(self.col_srclk, GPIO.LOW)
            sleep(self._com_delay)
            GPIO.output(self.col_srclk, GPIO.HIGH)

            mask = 1 << c
            for r in range(8):
                GPIO.output(self.row_srclk, GPIO.LOW)
                if self._data[r] & mask:
                    GPIO.output(self.row_ser, GPIO.HIGH)
                sleep(self._com_delay)
                GPIO.output(self.row_srclk, GPIO.HIGH)
                GPIO.output(self.row_ser, GPIO.LOW)
                sleep(self._com_delay)

            # col stays low from now on, we're scanning it
            GPIO.output(self.col_ser, GPIO.LOW)
            GPIO.output(self.latch, GPIO.HIGH)
            sleep(delay)


display = Display(col_srclk=matrix[0], latch=matrix[1], col_ser=matrix[2],
                  row_srclk=matrix[3], row_ser=matrix[4])

print 'test'
display.test()
sleep(1)
print 'reset'
display.reset()
sleep(1)

print 'start'
display.start()
display.set([0xf0] * 4 + [0x0f] * 4)
sleep(2)
display.set([0x0f] * 4 + [0xf0] * 4)
sleep(2)
display.set([
    0b11111111,
    0b01000000,
    0b00100000,
    0b00010000,
    0b00001000,
    0b00000100,
    0b00000010,
    0b11111111,
])
sleep(2)

for ch in ('Hello World!'):
    data = list(font8x8_basic[ord(ch)])
    # font8x8_basic data is bottom-to-top...
    data.reverse()
    display.set(data)
    sleep(0.5)

print 'stop'
display.stop()
print 'stopped'

print 'cleanup'
GPIO.cleanup()
