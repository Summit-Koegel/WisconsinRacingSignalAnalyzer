from ADS7828 import *
from enum import Enum

class DialIndex(Enum):
    DIAL_LEFT = 4
    DIAL_RIGHT = 5

class Dial(InputDevice):
    def __init__(self, index: DialIndex, adc: ADS7828):
        # Check for invalid dial index
        if not isinstance(index, DialIndex):
            raise TypeError("Index must be an instance of DialIndex")

        super().__init__()

        # Set lookup table to use
        if DialIndex == DIAL_LEFT:
            self.dial_lut = self.dial_left_lut
        else:
            self.dial_lut = self.dial_right_lut

        self.adc = adc
        self.index = index
        self.dial_pos = 0

    # Convert ADC count to dial position from the lookup table
    def adc_to_dial_pos(self, adc_count):
        for key, value in self.dial_lut.items():
            start, end = key
            if start <= adc_count <= end:
                return value

        return 0

    # Get dial position from 1 to 11
    def read_dial_state(self) -> int:
        # Read ADC and convert to dial position
        new_dial_pos = self.adc_to_dial_pos(self.adc.read_raw_adc(self.index), self.dial_lut)

        # Use old dial position for unmapped ADC readings
        self.dial_pos = self.dial_pos if new_dial_pos == 0 else new_dial_pos

        return self.dial_pos

    # Lookup table for left dial
    self.dial_left_lut = {
        (2638, 2700): 1, # 2650
        (2620, 2637): 2, # 2638
        (2500, 2540): 3, # 2520
        (2300, 2380): 4, # 2340
        (2050, 2200): 5, # 2120
        (1800, 1900): 6, # 1840
        (1400, 1600): 7, # 1500
        (900, 1200): 8, # 1096
        (550, 700): 9, # 596
        (50, 200): 10, # 92
        (0, 25): 11 # 3
    }

    # Lookup table for right dial
    self.dial_right_lut = {
        (1950, 2000): 1, # 1970
        (1900, 1945): 2, # 1935
        (1650, 1800): 3, # 1732
        (1400, 1550): 4, # 1492
        (1200, 1300): 5, # 1224
        (900, 1050): 6, # 975
        (650, 750): 7, # 707
        (400, 600): 8, # 463
        (200, 300): 9, # 232
        (20, 80): 10, # 37
        (0, 15): 11 # 1
    }