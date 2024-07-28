DEBUG = True
import time
import copy

if (DEBUG): print("   Importing PCA59XX")
from gpio.PCA95XX import *
from gpio.ioStruct import IoStruct
from can.mcpDriver import *
# from gpio.dial import ADS7828
from can.canStruct import *

INPUT_MODE = 1

lcStartTime = 0

# imports for GPIO functionality
# All button data and functions
class Buttons:
    def __init__(self):
        # Init PCA expander
        self.PCA = PCA95XX(1, 0x74, 16)
        #self.can = McpCanBus()
        self.adc = ADS7828()
        # Sotre button states: clearFaults, cycleScreen, RTD, yawCorrect, button5, button6
        self.buttonArray = [False, False, False, False, False, False] # this could probably be a dictionary, with the callback functions
        self.buttonMap = {0: False, 1: False, 2: False, 3: False, 4: False, 6: False}
        # Config pins on GPIO expander
        for i in range (0,16):
            self.PCA.config(pin=i, mode=INPUT_MODE)
            self.PCA.polarity(pin=i, value=True)

    def update_can_message(self, ioStruct):
        msg = [0x00, 0x00, 0x00]

        # Buttons
        if ioStruct.buttonOne:
            msg[0] |= 1 << 0
        if ioStruct.buttonTwo:
            msg[0] |= 1 << 1
        if ioStruct.buttonThree:
            msg[0] |= 1 << 2
        if ioStruct.buttonFour:
            msg[0] |= 1 << 3
        if ioStruct.buttonFive:
            msg[0] |= 1 << 4
        if ioStruct.buttonSix:
            msg[0] |= 1 << 5

        # Joystick
        if ioStruct.joystickCentre:
            msg[0] |= 1 << 6
        if ioStruct.joystickDown:
            msg[0] |= 1 << 7
        if ioStruct.joystickLeft:
            msg[1] |= 1 << 0
        if ioStruct.joystickRight:
            msg[1] |= 1 << 1
        if ioStruct.joystickUp:
            msg[1] |= 1 << 2

        # Dial left
        dialLeftValue = ioStruct.dialLeft & 0x0F
        msg[1] |= dialLeftValue << 3

        # Dial right
        dialRightValue = ioStruct.dialRight & 0x0F
        msg[2] |= dialRightValue

        return msg

    def readButtons(self, ioStruct):
        global lcStartTime

        modification = False

        ioStructOld = copy.copy(ioStruct)

        ioStruct.buttonOne = bool(self.PCA.input(0))
        ioStruct.buttonTwo = bool(self.PCA.input(1))
        ioStruct.buttonThree = bool(self.PCA.input(3))
        ioStruct.buttonFour = bool(self.PCA.input(2))
        ioStruct.buttonFive = bool(self.PCA.input(4))
        ioStruct.buttonSix = bool(self.PCA.input(6))
        if ioStruct.buttonSix:
            lcStartTime = time.time()

        if int(time.time() - lcStartTime) > 5:
            lcStartTime = 0
        else:
            ioStruct.buttonSix = True

        ioStruct.joystickUp = bool(self.PCA.input(8))
        ioStruct.joystickDown = bool(self.PCA.input(9))
        ioStruct.joystickLeft = bool(self.PCA.input(7))
        ioStruct.joystickRight = bool(self.PCA.input(5))
        ioStruct.joystickCentre = bool(self.PCA.input(11))

        newDialLeft = self.adc_to_dial_pos(self.adc.read_raw_adc(4), self.dial_left)
        newDialRight = self.adc_to_dial_pos(self.adc.read_raw_adc(5), self.dial_right)

        msg = self.update_can_message(ioStruct)
        #msg = (0xFF, 0xFF, 0xFF)

        can.txMessage(0x350, 3, msg, False)

        return ioStructOld == ioStruct

        #for i in range(4, 9):
        # newVal = bool(self.PCA.input(i))
        # if (self.buttonArray[i - 4] != newVal):
        #     self.buttonArray[i - 4] = newVal
        #     print('Button pressed: ' + str(i))
        #     modification = True
        # for key in self.buttonMap:
        #     currentState = bool(self.PCA.input(key))
        #     # logic for detecting only the unpressed to pressed state, previous implementations activated the button for both transitions
        #     if not self.buttonMap[key] and currentState:
        #         self.buttonMap[key] = currentState
        #         print(f'Button {key} pressed')
        #         modification = True
        #     else:
        #         self.buttonMap[key] = currentState

        #return modification

    # Assuming ioStruct is an instance of IoStruct
