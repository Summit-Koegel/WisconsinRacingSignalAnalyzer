# a state machine for handiling outside stimulus
# and utilizing it to generate screens
DEBUG = True
EV_MODE = False
ON_PI = False

from time import sleep, time
if ON_PI:
    from sleep_until import sleep_until

if(DEBUG): print("         Importing tkinter")
from tkinter import *
if(DEBUG): print("         Importing driveDisplay")
from display.ccarDisplay import *
from display.ecarDisplay import *

if(DEBUG): print("   Importing GPIO struct")
#import gpio.ioStruct as ioStruct
if(DEBUG): print("   Importing CAN struct")
import can.canStruct as canStruct

if(DEBUG): print("   Importing Screen")
from enum import Enum

dLeft = 0

class displayStateMachine:
    # object for holding all external stimuli
    def __init__(self):
        # Create a display data object for updating later
        if EV_MODE:
            self.canDataIn = canStruct.ElectricStruct()
            self.canDataOut = canStruct.ElectricStruct()
        else:
            self.canDataIn = canStruct.CombustionStruct()
            self.canDataOut = canStruct.CombustionStruct()

        # Create all of the screens
        self.screen = Tk()
        self.width = self.screen.winfo_screenwidth()
        self.height = self.screen.winfo_screenheight()
        # root window title and dimension
        self.screen.maxsize(self.width, self.height)

        # Intialize the screens
        if EV_MODE:
            self.display = EcarDisplay(self.screen, self.width, self.height)
        else:
            self.display = CcarDisplay(self.screen, self.width, self.height)
        # Set screen to fullscreen
        if ON_PI: self.screen.attributes('-fullscreen', True)

    def readGpioStimuli(self, ioPipe):
        # Empty the I/O pipe
        while (not(ioPipe.empty())):
            global dLeft
            self.ioData = ioPipe.get()
            dLeft = self.ioData.dialLeft

    def readCanStimuli(self, canPipe):
        # Empty the CAN pipe
        while (not(canPipe.empty())):
            self.canDataIn = canPipe.get()

##
# @Brief Operate the data flow and control loop of the display
#
# @canPipe SimpleQueue that will pass CAN data
#
def runDisplay(canPipe, ioPipe):
    runtime = time()
    displaySM = displayStateMachine()

    while (True):
        if ((time() - runtime) > 0.1):
            runtime = time()

            global dLeft
            displaySM.canDataIn._HW_SENSORS_CAN_TC = dLeft

            displaySM.display.updateDisplay(displaySM.canDataIn)

            displaySM.screen.update_idletasks()
            displaySM.screen.update()

            displaySM.readCanStimuli(canPipe)
            displaySM.readGpioStimuli(ioPipe)
        else:
            if ON_PI:
                sleep_until(runtime + 0.1)
            else:
                sleep(0.01)

class ScreenState(Enum):
    Drive = 0

