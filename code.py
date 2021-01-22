# install adafruit HID library to use keyboard functionality
# see https://github.com/adafruit/Adafruit_CircuitPython_Bundle/releases

import os
import time
import board
import touchio
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS

#init touch buttons
touch1 = touchio.TouchIn(board.A0)
touch2 = touchio.TouchIn(board.A1)
touch3 = touchio.TouchIn(board.A2)

#init led lines
ledG = DigitalInOut(board.D5)
ledG.direction = Direction.OUTPUT
ledR = DigitalInOut(board.D6)
ledR.direction = Direction.OUTPUT
ledB = DigitalInOut(board.D7)
ledB.direction = Direction.OUTPUT

time.sleep(1)  # Sleep for a bit to avoid a race condition on some systems

kbd = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(kbd)

print("starting...")

chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ012345678901"

while True:
    if touch1.raw_value > 2500 or touch2.raw_value > 2500 or touch3.raw_value > 2500:
        for x in range(10):
            rv = (touch1.raw_value&0x3) | ((touch2.raw_value&0x3)<<2) | ((touch3.raw_value&0x3)<<4)
            # print("%d\n" % rv)
            layout.write(chars[rv])
            ledR.value = rv&0x01
            ledG.value = rv&0x04
            ledB.value = rv&0x10
            time.sleep(0.05)
            ledR.value = True
            ledG.value = True
            ledB.value = True
            time.sleep(0.05)
        layout.write('\n')
    else:
        ledR.value = True
        ledG.value = True
        ledB.value = True
    time.sleep(0.1)



