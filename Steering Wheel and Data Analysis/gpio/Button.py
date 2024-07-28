import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time 
from callback_framework.initial import InputDevice
from enum import Enum
from gpio.PCA95XX import *

class ButtonIndex(Enum):
    BUTTON_ONE = 0
    BUTTON_TW0 = 1
    BUTTON_THREE = 3
    BUTTON_FOUR = 2
    BUTTON_FIVE = 4
    BUTTON_SIX = 6

    
class Button(InputDevice):
    def __init__(self, index: ButtonIndex, PCA: PCA95XX):
        """Button class should have indices only as defined in the Index Enum class
        """
        if not isinstance(index, ButtonIndex):
            raise TypeError("Index must be an instance of Index Enum, defined in the Button class")
        
        super().__init__()
        self.PCA = PCA
        self.state = False
        self.index = index
    
    def read_button_state(self) -> bool:
        current_state = bool(self.PCA.input(self.index.value))

        if not self.state and current_state:
            self.state = True
            self.run_callback()
        elif self.state and not current_state:
            self.state = False
    
        return current_state

def sample_function(button: Button):
    print(f"Button {button.index.value} was pressed!")

# PCA = PCA95XX(1, 0x74, 16)

# test_button = Button(ButtonIndex.BUTTON_ONE, PCA)
# test_button.register_callback(sample_function, test_button)

# while True:
#     test_button.read_button_state()
#     time.sleep(0.01)