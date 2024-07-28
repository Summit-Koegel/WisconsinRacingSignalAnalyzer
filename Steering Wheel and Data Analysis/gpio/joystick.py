import random
# Operations and data relating to the dpad
class joystick:    
    def __init__(self, x, y):
        self._dpadX = x
        self._dpadY = y

    def readDpad(self):
        while (True):
            self._dpadX = random.choice([-1, 0, 1])
            self._dpadY = random.choice([-1, 0, 1])
