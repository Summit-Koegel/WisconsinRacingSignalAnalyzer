DEBUG = True

if(DEBUG): print("      Importing tkinter")
from tkinter import *
from tkinter import ttk
if(DEBUG): print("      Importing Display struct")
import can.canStruct
from random import randint

class CcarDisplay:
    def __init__(self, frame, width, height):
        # Define the width and height of the smallest frames
        frameWidth = width/5
        frameHeight = height/3
        # Dark Mode
        ttk.Style().configure('Dark.TFrame', foreground='white', background='#001a33', relief='solid')
        ttk.Style().configure('DarkLabel.TLabel', foreground='white', background='#001a33', font=("Daytona", 10))
        ttk.Style().configure('DarkValueSmall.TLabel', foreground='white', background='#001a33', font=("Daytona", 16))
        ttk.Style().configure('DarkValueMedium.TLabel', foreground='white', background='#001a33', font=("Daytona", 32))
        ttk.Style().configure('DarkValueLarge.TLabel', foreground='white', background='#001a33', font=("Daytona", 72))
        # Magenta Mode
        ttk.Style().configure('Magenta.TFrame', foreground='white', background='#800080', relief='solid')
        ttk.Style().configure('MagentaLabel.TLabel', foreground='white', background='#800080', font=("Daytona", 10))
        ttk.Style().configure('MagentaValueSmall.TLabel', foreground='white', background='#800080', font=("Daytona", 16))
        ttk.Style().configure('MagentaValueMedium.TLabel', foreground='white', background='#800080', font=("Daytona", 32))
        ttk.Style().configure('MagentaValueLarge.TLabel', foreground='white', background='#800080', font=("Daytona", 72))
        # Red Mode
        ttk.Style().configure('Red.TFrame', foreground='white', background='#660000', relief='solid')
        ttk.Style().configure('RedLabel.TLabel', foreground='white', background='#660000', font=("Daytona", 10))
        ttk.Style().configure('RedValueSmall.TLabel', foreground='white', background='#660000', font=("Daytona", 16))
        ttk.Style().configure('RedValueMedium.TLabel', foreground='white', background='#660000', font=("Daytona", 32))
        ttk.Style().configure('RedValueLarge.TLabel', foreground='white', background='#660000', font=("Daytona", 72))
        # Define the frames
        # Left Column
        self.oilFrame = ttk.Frame(frame, width=frameWidth, height=frameHeight, style='Dark.TFrame')
        self.vbatFrame = ttk.Frame(frame, width=frameWidth, height=frameHeight, style='Dark.TFrame')
        self.lcFrame = ttk.Frame(frame, width=frameWidth, height=frameHeight, style='Dark.TFrame')
        # Middle Column
        self.rpmFrame = ttk.Frame(frame, width=3*frameWidth, height=frameHeight, style='Dark.TFrame')
        self.gearFrame = ttk.Frame(frame, width=3*frameWidth, height=2*frameHeight, style='Dark.TFrame')
        # Right Column
        self.fuelPressureFrame = ttk.Frame(frame, width = frameWidth, height = frameHeight, style='Dark.TFrame')
        self.ectFrame = ttk.Frame(frame, width = frameWidth, height = frameHeight, style='Dark.TFrame')
        self.tcFrame = ttk.Frame(frame, width = frameWidth, height = frameHeight, style='Dark.TFrame')

        # Define data displayed
        self.oilPressure = IntVar(self.oilFrame, 0)
        self.lc = IntVar(self.lcFrame, 0)
        self.vbat = IntVar(self.vbatFrame, 0)

        self.rpm = IntVar(self.rpmFrame, 0)
        #img = ImageTk.PhotoImage(Image.open("Pictures/forest.jpg"))

        self.gear = IntVar(self.gearFrame, 0)
        self.neutral = StringVar(self.gearFrame, '')

        self.fuelPressure = IntVar(self.fuelPressureFrame, 0)
        self.ect = IntVar(self.ectFrame, 0)
        self.tc = IntVar(self.tcFrame, 0)

        self.createLabels()

        # Place left column
        self.oilFrame.grid(row = 0, column = 0)
        self.vbatFrame.grid(row = 1, column = 0)
        self.lcFrame.grid(row = 2, column = 2)

        #Place middle column
        self.rpmFrame.grid(row = 0, column = 1)
        self.gearFrame.grid(row = 1, column = 1, rowspan = 2)

        # Place right column
        self.fuelPressureFrame.grid(row = 0, column = 2)
        self.ectFrame.grid(row = 1, column = 2)
        self.tcFrame.grid(row = 2, column = 0)

    def createLabels(self):
        # Create Labels
        # Left Column Labels
        self.oilLabel = ttk.Label(self.oilFrame, text='Oil Pressure', style='DarkLabel.TLabel')
        self.oilLabel.place(anchor=NW, relx=0.05, rely=0.05)
        self.oilValue = ttk.Label(self.oilFrame, textvariable=self.oilPressure, style='DarkValueSmall.TLabel')
        self.oilValue.place(anchor=SE, relx=0.9, rely=0.9)

        self.vbatLabel = ttk.Label(self.vbatFrame, text='VBAT', style='DarkLabel.TLabel')
        self.vbatLabel.place(anchor=NW, relx=0.05, rely=0.05)
        self.vbatValue = ttk.Label(self.vbatFrame, textvariable=self.vbat, style='DarkValueSmall.TLabel')
        self.vbatValue.place(anchor=SE, relx=0.9, rely=0.9)

        self.lcLabel = ttk.Label(self.lcFrame, text='LC', style='DarkLabel.TLabel')
        self.lcLabel.place(anchor=NW, relx=0.05, rely=0.05)
        self.lcValue = ttk.Label(self.lcFrame, textvariable=self.lc, style='DarkValueSmall.TLabel')
        self.lcValue.place(anchor=SE, relx=0.9, rely=0.9)

        # Middle Column Labels
        self.rpmLabel = ttk.Label(self.rpmFrame, text='RPM', style='DarkLabel.TLabel')
        self.rpmLabel.place(anchor=NW, relx=0.05, rely=0.05)
        self.rpmValue = ttk.Label(self.rpmFrame, textvariable=self.rpm, style='DarkValueMedium.TLabel')
        self.rpmValue.place(anchor=CENTER, relx=0.5, rely=0.65)

        self.gearLabel = ttk.Label(self.gearFrame, text='Gear', style='DarkLabel.TLabel')
        self.gearLabel.place(anchor=NW, relx=0.05, rely=0.05)
        self.gearValue = ttk.Label(self.gearFrame, textvariable=self.gear, style='DarkValueLarge.TLabel')
        self.gearValue.place(anchor=CENTER, relx=0.5, rely=0.5)
        self.neutralValue = ttk.Label(self.gearFrame, textvariable=self.neutral, style='DarkValueLarge.TLabel')
        self.neutralValue.place(anchor=CENTER, relx=0.5, rely=0.5)

        # Right Column Labels
        self.fuelPressureLabel = ttk.Label(self.fuelPressureFrame, text='Fuel Pressure', style='DarkLabel.TLabel')
        self.fuelPressureLabel.place(anchor=NW, relx=0.05, rely=0.05)
        self.fuelPressureValue = ttk.Label(self.fuelPressureFrame, textvariable=self.fuelPressure, style='DarkValueSmall.TLabel')
        self.fuelPressureValue.place(anchor=SE, relx=0.9, rely=0.9)

        ectLabel = ttk.Label(self.ectFrame, text='ECT', style='DarkLabel.TLabel')
        ectLabel.place(anchor=NW, relx=0.05, rely=0.05)
        ectValue = ttk.Label(self.ectFrame, textvariable=self.ect, style='DarkValueSmall.TLabel')
        ectValue.place(anchor=SE, relx=0.9, rely=0.9)

        #tcLabel = ttk.Label(self.tcFrame, text='TC', style='DarkLabel.TLabel')
        tcLabel = ttk.Label(self.tcFrame, text='O2', style='DarkLabel.TLabel')
        tcLabel.place(anchor=NW, relx=0.05, rely=0.05)
        tcValue = ttk.Label(self.tcFrame, textvariable=self.tc, style='DarkValueSmall.TLabel')
        tcValue.place(anchor=SE, relx=0.9, rely=0.9)

    def updateDisplay(self, driveData):
        self.rpm.set(driveData._HW_Sensors_RPM - (driveData._HW_Sensors_RPM % 10))
        self.vbat.set(driveData._HW_Sensors_SysVolt)
        #self.lc.set(driveData._HW_SENSORS_CAN_LC)
        self.lc.set(driveData._HW_Actuators_Inj_Cyl2_InjMPW)
        self.oilPressure.set(driveData._HW_Sensors_EOP)
        self.ect.set(driveData._HW_Sensors_ECT * 100)
        self.fuelPressure.set(driveData._HW_SENSORS_Fuel_Pressure )
        #self.tc.set(driveData._HW_SENSORS_CAN_TC)
        self.tc.set(driveData._Virtual_Sensors_Cyl1_UEGO / 100)

        # Set gears
        if (driveData._HW_Sensors_Gear == 0):
            self.neutral.set("N")
            self.gear.set(0)
            self.neutralValue.place(anchor=CENTER, relx=0.5, rely=0.5)
        else:
            self.gear.set(driveData._HW_Sensors_Gear)
            self.neutral.set("")
            self.neutralValue.place_forget()
        # Set pressure color
        if (driveData._HW_SENSORS_Fuel_Pressure < 50):
            self.fuelPressureFrame['style'] = 'Red.TFrame'
            self.fuelPressureLabel['style'] = 'RedLabel.TLabel'
            self.fuelPressureValue['style'] = 'RedValueSmall.TLabel'
        elif (driveData._HW_SENSORS_Fuel_Pressure < 100):
            self.fuelPressureFrame['style'] = 'Magenta.TFrame'
            self.fuelPressureLabel['style'] = 'MagentaLabel.TLabel'
            self.fuelPressureValue['style'] = 'MagentaValueSmall.TLabel'
        else:
            self.fuelPressureFrame['style'] = 'Dark.TFrame'
            self.fuelPressureLabel['style'] = 'DarkLabel.TLabel'
            self.fuelPressureValue['style'] = 'DarkValueSmall.TLabel'
        # Set vbat color
        if (driveData._HW_Sensors_SysVolt < 11 or driveData._HW_Sensors_SysVolt > 15):
            self.vbatFrame['style'] = 'Red.TFrame'
            self.vbatLabel['style'] = 'RedLabel.TLabel'
            self.vbatValue['style'] = 'RedValueSmall.TLabel'
        elif (driveData._HW_Sensors_SysVolt < 12 or driveData._HW_Sensors_SysVolt > 14):
            self.vbatFrame['style'] = 'Magenta.TFrame'
            self.vbatLabel['style'] = 'MagentaLabel.TLabel'
            self.vbatValue['style'] = 'MagentaValueSmall.TLabel'
        else:
            self.vbatFrame['style'] = 'Dark.TFrame'
            self.vbatLabel['style'] = 'DarkLabel.TLabel'
            self.vbatValue['style'] = 'DarkValueSmall.TLabel'
