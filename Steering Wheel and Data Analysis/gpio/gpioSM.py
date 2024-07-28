import time
DEBUG = True

if (DEBUG): print("   Importing GPIO struct")
from gpio.ioStruct import IoStruct

if (DEBUG): print("   Importing CAN struct")
from can.canStruct import *

if (DEBUG): print("   Importing GPIO LED")
from gpio.led import LedBar

if (DEBUG): print("   Importing GPIO Buttons")
from gpio.buttons import Buttons

if (DEBUG): print("    Importing PCA95XX")
from gpio.PCA95XX import PCA95XX

from gpio.Button import Button, ButtonIndex, sample_function

EV_MODE = False

MOTOR_WARNING_TEMP = 80
MOTOR_ERROR_TEMP = 100

CELL_WARNING_VOLTAGE = 3.5
CELL_ERROR_VOLTAGE = 3.3

CELL_WARNING_TEMPERATURE = 50
CELL_ERROR_TEMPERATURE = 60

class gpioStateMachine:
    def __init__(self):
        self.PCA = PCA95XX(1, 0x74, 16)
        self.ioStruct = IoStruct()
        self.leds = LedBar()
        if EV_MODE:
            self.canDataIn = ElectricStruct()
        else:
            self.canDataIn = CombustionStruct()
        # Establish I/O Expander buttons
        #self.buttons = Buttons()

        button_one = Button(ButtonIndex.BUTTON_ONE, self.PCA)
        button_two = Button(ButtonIndex.BUTTON_TW0, self.PCA)
        button_three = Button(ButtonIndex.BUTTON_THREE, self.PCA)
        button_four = Button(ButtonIndex.BUTTON_FOUR, self.PCA)
        button_five = Button(ButtonIndex.BUTTON_FIVE, self.PCA)
        button_six = Button(ButtonIndex.BUTTON_SIX, self.PCA)

        button_one.register_callback(sample_function, button_one)
        button_two.register_callback(sample_function, button_two)
        button_three.register_callback(sample_function, button_three)
        button_four.register_callback(sample_function, button_four)
        button_five.register_callback(sample_function, button_five)
        button_six.register_callback(sample_function, button_six)
        
        self.buttons = [
            button_one, 
            button_two,
            button_three,
            button_four,
            button_five,
            button_six
        ]

    def readADC(self, ioPipeCAN, ioPipeDisplay):
        None

    def readButtons(self, ioPipeCAN, ioPipeDisplay):
        # if (self.buttons.readButtons(self.ioStruct)):
        #     #print(self.ioStruct)
        #     time.sleep(0.1)
        #     ioPipeCAN.put(self.ioStruct)
        #     ioPipeDisplay.put(self.ioStruct)

        for button in self.buttons:
            button.read_button_state()
            time.sleep(0.01)

    def exportData(self, ioPipeCAN, ioPipeDisplay):
        ioPipeCAN.put(self.ioStruct)
        ioPipeDisplay.put(self.ioStruct)

    def readCanStimuli(self, canPipe):
        # Empty the CAN pipe
        while (not(canPipe.empty())):
            self.canDataIn = canPipe.get()

        if EV_MODE:
            try:
                if((self.canDataIn.High_Cell_Temp >= CELL_ERROR_TEMPERATURE) or
                (self.canDataIn.Low_Cell_Voltage <= CELL_ERROR_VOLTAGE) or
                (self.canDataIn.IRL_T_winding >= MOTOR_ERROR_TEMP)or
                (self.canDataIn.IRR_T_winding >= MOTOR_ERROR_TEMP)):
                    self.leds.setError()
                elif((self.canDataIn.High_Cell_Temp >= CELL_WARNING_TEMPERATURE) or
                (self.canDataIn.Low_Cell_Voltage <= CELL_WARNING_VOLTAGE) or
                (self.canDataIn.IRL_T_winding >= MOTOR_WARNING_TEMP)or
                (self.canDataIn.IRR_T_winding >= MOTOR_WARNING_TEMP)):
                    self.leds.setWarning()
                else:
                    self.leds.setOff()
            except Exception as e:
                print(str(e))
                None
        else:
            self.leds.updateLEDBar(self.canDataIn._HW_Sensors_RPM)

def runGPIO(canPipeIo, ioPipeCAN, ioPipeDisplay):
    gpioSM = gpioStateMachine()

    while (True):
        # Harvest values
        try:
            gpioSM.readADC(ioPipeCAN, ioPipeDisplay)
        except Exception as e:
            print(str(e))
            None
        try:
            gpioSM.readButtons(ioPipeCAN, ioPipeDisplay)
        except Exception as e:
            print(str(e))
            None
        try:
            gpioSM.readCanStimuli(canPipeIo)
        except Exception as e:
            print(str(e))
            None
