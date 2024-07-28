DEBUG = True

from tkinter import *
from tkinter import ttk

from can.canStruct import *

PERCENT_MODE = True

INVERTER_MIN_TEMP = 0
INVERTER_WARNING_TEMP = 80
INVERTER_ERROR_TEMP = 100

MOTOR_WARNING_TEMP = 80
MOTOR_ERROR_TEMP = 100

CELL_HIGH_VOLTAGE = 4.15
CELL_WARNING_VOLTAGE = 3.5
CELL_ERROR_VOLTAGE = 3.3

CELL_LOW_TEMPERATURE = 25
CELL_WARNING_TEMPERATURE = 50
CELL_ERROR_TEMPERATURE = 60

class EcarDisplay:
    def __init__(self, frame, width, height):
        # Define the width and height of the smallest frames
        frameWidth = width/2
        frameHeight = height/3
        # Dark Mode
        ttk.Style().configure('Dark.TFrame', foreground='white', background='#001a33', relief='solid')
        ttk.Style().configure('DarkLabel.TLabel', foreground='white', background='#001a33', font=("Daytona", 10))
        ttk.Style().configure('DarkValueSmall.TLabel', foreground='white', background='#001a33', font=("Daytona", 16))
        ttk.Style().configure('DarkValueMedium.TLabel', foreground='white', background='#001a33', font=("Daytona", 32))
        ttk.Style().configure('DarkValueLarge.TLabel', foreground='white', background='#001a33', font=("Daytona", 72))
        # Yellow Mode
        ttk.Style().configure('Yellow.TFrame', foreground='black', background='#ffff00', relief='solid')
        ttk.Style().configure('YellowLabel.TLabel', foreground='black', background='#ffff00', font=("Daytona", 10))
        ttk.Style().configure('YellowValueSmall.TLabel', foreground='black', background='#ffff00', font=("Daytona", 16))
        ttk.Style().configure('YellowValueMedium.TLabel', foreground='black', background='#ffff00', font=("Daytona", 32))
        ttk.Style().configure('YellowValueLarge.TLabel', foreground='black', background='#ffff00', font=("Daytona", 72))
        # Red Mode
        ttk.Style().configure('Red.TFrame', foreground='white', background='#ff0000', relief='solid')
        ttk.Style().configure('RedLabel.TLabel', foreground='white', background='#ff0000', font=("Daytona", 10))
        ttk.Style().configure('RedValueSmall.TLabel', foreground='white', background='#ff0000', font=("Daytona", 16))
        ttk.Style().configure('RedValueMedium.TLabel', foreground='white', background='#ff0000', font=("Daytona", 32))
        ttk.Style().configure('RedValueLarge.TLabel', foreground='white', background='#ff0000', font=("Daytona", 72))
        # Define the frames
        ############
        # Top Row #
        ##########
        self.cellVoltageFrame = ttk.Frame(frame, width=frameWidth*2, height=frameHeight, style='Dark.TFrame')
        self.cellTempFrame = ttk.Frame(frame, width=frameWidth*2, height=frameHeight, style='Dark.TFrame')
        self.rlTempFrame = ttk.Frame(frame, width=frameWidth, height=frameHeight, style='Dark.TFrame')
        self.rrTempFrame = ttk.Frame(frame, width=frameWidth, height=frameHeight, style='Dark.TFrame')
        ##########################
        # Define data displayed #
        ########################
        self.cellVoltage = DoubleVar(self.cellVoltageFrame, 0)
        self.cellTemp = DoubleVar(self.cellTempFrame, 0)
        self.rlTemp = IntVar(self.rlTempFrame, 0)
        self.rrTemp = IntVar(self.rrTempFrame, 0)
    
        self.createLabels()
        ####################
        # Grid the frames #
        ##################
        self.cellVoltageFrame.grid(row = 0, column = 0, columnspan=2)
        self.cellTempFrame.grid(row = 1, column = 0, columnspan=2)
        self.rlTempFrame.grid(row = 2, column = 0)
        self.rrTempFrame.grid(row = 2, column = 1)

    def createLabels(self):
        # Inverter Labels
        self.cellVoltageLabel = ttk.Label(self.cellVoltageFrame, text='Lowest Voltage', style='DarkLabel.TLabel')
        self.cellVoltageLabel.place(anchor=NW, relx=0.025, rely=0.025)
        self.cellVoltageValue = ttk.Label(self.cellVoltageFrame, textvariable=self.cellVoltage, style='DarkValueMedium.TLabel')
        self.cellVoltageValue.place(anchor=CENTER, relx=0.5, rely=0.5)
        self.cellTempLabel = ttk.Label(self.cellTempFrame, text='Highest Cell Temp', style='DarkLabel.TLabel')
        self.cellTempLabel.place(anchor=NW, relx=0.025, rely=0.025)
        self.cellTempValue = ttk.Label(self.cellTempFrame, textvariable=self.cellTemp, style='DarkValueSmall.TLabel')
        self.cellTempValue.place(anchor=CENTER, relx=0.5, rely=0.5)
        self.rlTempLabel = ttk.Label(self.rlTempFrame, text='RL Temp', style='DarkLabel.TLabel')
        self.rlTempLabel.place(anchor=NW, relx=0.05, rely=0.05)
        self.rlTempValue = ttk.Label(self.rlTempFrame, textvariable=self.rlTemp, style='DarkValueSmall.TLabel')
        self.rlTempValue.place(anchor=CENTER, relx=0.5, rely=0.5)
        self.rrTempLabel = ttk.Label(self.rrTempFrame, text='RR Temp', style='DarkLabel.TLabel')
        self.rrTempLabel.place(anchor=NW, relx=0.05, rely=0.05)
        self.rrTempValue = ttk.Label(self.rrTempFrame, textvariable=self.rrTemp, style='DarkValueSmall.TLabel')
        self.rrTempValue.place(anchor=CENTER, relx=0.5, rely=0.5)

    def updateDisplay(self, driveData: ElectricStruct):
        if (PERCENT_MODE):
            # Deal with cell voltages
            if (driveData.Low_Cell_Voltage >= CELL_HIGH_VOLTAGE):
                self.cellVoltage.set(100)
            elif(driveData.Low_Cell_Voltage <= CELL_ERROR_VOLTAGE):
                self.cellVoltage.set(0)
            else:
                self.cellVoltage.set(int(float(driveData.Low_Cell_Voltage - CELL_ERROR_VOLTAGE) / float(CELL_HIGH_VOLTAGE - CELL_ERROR_VOLTAGE) * 100))
            
            # Deal with cell temps
            if (driveData.High_Cell_Temp <= CELL_LOW_TEMPERATURE):
                self.cellTemp.set(100)
            elif(driveData.High_Cell_Temp >= CELL_ERROR_TEMPERATURE):
                self.cellTemp.set(0)
            else:
                self.cellTemp.set(int(float(CELL_ERROR_TEMPERATURE - driveData.High_Cell_Temp) / float(CELL_ERROR_TEMPERATURE - CELL_LOW_TEMPERATURE) * 100))
        else:
            self.cellVoltage.set(driveData.Low_Cell_Voltage)
            self.cellTemp.set(driveData.High_Cell_Temp)
        # Update motor temps
        self.rlTemp.set(driveData.IRL_T_winding)
        self.rrTemp.set(driveData.IRR_T_winding)
        ########################
        # Set status colors #
        ######################
        # Cell voltage colors
        if (driveData.Low_Cell_Voltage <= CELL_ERROR_VOLTAGE):
            self.cellVoltageFrame['style'] = 'Red.TFrame'
            self.cellVoltageValue['style'] = 'RedValueMedium.TLabel'
            self.cellVoltageLabel['style'] = 'RedLabel.TLabel'
        elif (driveData.Low_Cell_Voltage <= CELL_WARNING_VOLTAGE):
            self.cellVoltageFrame['style'] = 'Yellow.TFrame'
            self.cellVoltageValue['style'] = 'YellowValueMedium.TLabel'
            self.cellVoltageLabel['style'] = 'YellowLabel.TLabel'
        else:
            self.cellVoltageFrame['style'] = 'Dark.TFrame'
            self.cellVoltageValue['style'] = 'DarkValueMedium.TLabel'
            self.cellVoltageLabel['style'] = 'DarkLabel.TLabel'
        # Cell temperature colors
        if (driveData.High_Cell_Temp >= CELL_ERROR_TEMPERATURE):
            self.cellTempFrame['style'] = 'Red.TFrame'
            self.cellTempValue['style'] = 'RedValueMedium.TLabel'
            self.cellTempLabel['style'] = 'RedLabel.TLabel'
        elif (driveData.High_Cell_Temp >= CELL_WARNING_TEMPERATURE):
            self.cellTempFrame['style'] = 'Yellow.TFrame'
            self.cellTempValue['style'] = 'YellowValueMedium.TLabel'
            self.cellTempLabel['style'] = 'YellowLabel.TLabel'
        else:
            self.cellTempFrame['style'] = 'Dark.TFrame'
            self.cellTempValue['style'] = 'DarkValueMedium.TLabel'
            self.cellTempLabel['style'] = 'DarkLabel.TLabel'
        ########################
        # Set motor colors #
        ######################
        # Rear Left
        if (driveData.IRL_T_winding >= MOTOR_ERROR_TEMP):
            self.rlTempFrame['style'] = 'Red.TFrame'
            self.rlTempValue['style'] = 'RedValueSmall.TLabel'
            self.rlTempLabel['style'] = 'RedLabel.TLabel'
        elif (driveData.IRL_T_winding >= MOTOR_WARNING_TEMP):
            self.rlTempFrame['style'] = 'Yellow.TFrame'
            self.rlTempValue['style'] = 'YellowValueSmall.TLabel'
            self.rlTempLabel['style'] = 'YellowLabel.TLabel'
        else:
            self.rlTempFrame['style'] = 'Dark.TFrame'
            self.rlTempValue['style'] = 'DarkValueSmall.TLabel'
            self.rlTempLabel['style'] = 'DarkLabel.TLabel'
        # Rear Right
        if (driveData.IRR_T_winding >= MOTOR_ERROR_TEMP):
            self.rrTempFrame['style'] = 'Red.TFrame'
            self.rrTempValue['style'] = 'RedValueSmall.TLabel'
            self.rrTempLabel['style'] = 'RedLabel.TLabel'
        elif (driveData.IRR_T_winding >= MOTOR_WARNING_TEMP):
            self.rrTempFrame['style'] = 'Yellow.TFrame'
            self.rrTempValue['style'] = 'YellowValueSmall.TLabel'
            self.rrTempLabel['style'] = 'YellowLabel.TLabel'
        else:
            self.rrTempFrame['style'] = 'Dark.TFrame'
            self.rrTempValue['style'] = 'DarkValueSmall.TLabel'
            self.rrTempLabel['style'] = 'DarkLabel.TLabel'
