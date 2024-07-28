import board
import neopixel

from time import time

EV_MODE = True

LIGHTS_START = 4500
SHIFT_INDICATION = 8500

WARNING_TEMP = 50
ERROR_TEMP = 60

NUM_LEDS = 12

RED =    (255, 0, 0)
ORANGE = (255, 127, 0)
YELLOW = (255, 255, 0)
GREEN =  (0, 255, 0)
BLUE =   (0, 0, 255)
PURPLE = (255, 0, 255)
OFF =    (0, 0, 0)

class LedBar:    
    def __init__(self):
        self.bar = neopixel.NeoPixel(board.D18, 12)
        self.blinkBool = True
        self.lastBlink = time()

    def setGood(self):
        for count in range(0, 12):
            self.bar[count] = GREEN

    def setWarning(self):
        for count in range(0, 12):
            self.bar[count] = YELLOW
    
    def setError(self):
        for count in range(0, 12):
            self.bar[count] = RED

    def setOff(self):
        for count in range(0, 12):
            self.bar[count] = OFF

    def updateLEDBar(self, value):
        if ((time() - self.lastBlink) > 0.1):
            # Update time stamp, and flip state
            self.lastBlink = time()
            self.blinkBool = not self.blinkBool

        incVal = (SHIFT_INDICATION - LIGHTS_START) / NUM_LEDS

        if EV_MODE:
            for count in range(0, 12):
                # Check if LED should be onif (rpm > 10000):
                if (value > ERROR_TEMP):
                    if (self.blinkBool):
                        self.bar[count] = RED
                    else:
                        self.bar[count] = OFF
                elif (value > WARNING_TEMP):
                    self.bar[count] = ORANGE
                else:
                    self.bar[count] = OFF
        else:
            for count in range(0, 12):
                # Check if LED should be onif (rpm > 10000):
                if (value > SHIFT_INDICATION):
                    if (self.blinkBool):
                        self.bar[count] = RED
                    else:
                        self.bar[count] = OFF
                elif (value > (count * incVal + LIGHTS_START)):
                    if (count < 2):
                        self.bar[count] = PURPLE
                    elif (count < 4):
                        self.bar[count] = BLUE
                    elif (count < 6):
                        self.bar[count] = GREEN
                    elif (count < 8):
                        self.bar[count] = YELLOW
                    elif (count < 10):
                        self.bar[count] = ORANGE
                    else:
                        self.bar[count] = RED
                else:
                    self.bar[count] = OFF
                # Iterate over the entire LED bar
                count = count + 1
