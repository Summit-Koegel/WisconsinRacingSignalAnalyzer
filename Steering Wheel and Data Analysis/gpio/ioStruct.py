
class IoStruct:
    def __init__(self):
        # Dials
        self.dialLeft = 0
        self.dialRight = 0
        # Buttons
        self.buttonOne = False
        self.buttonTwo = False
        self.buttonThree = False
        self.buttonFour = False
        self.buttonFive = False
        self.buttonSix = False
        # Joystick
        self.joystickUp = False
        self.joystickDown = False
        self.joystickLeft = False
        self.joystickRight = False
        self.joystickCentre = False

    def __eq__(self, other):
        if not isinstance(other, IoStruct):
            return False

        # Compare all attributes for equality
        return (
            self.dialLeft == other.dialLeft
            and self.dialRight == other.dialRight
            and self.buttonOne == other.buttonOne
            and self.buttonTwo == other.buttonTwo
            and self.buttonThree == other.buttonThree
            and self.buttonFour == other.buttonFour
            and self.buttonFive == other.buttonFive
            and self.buttonSix == other.buttonSix
            and self.joystickUp == other.joystickUp
            and self.joystickDown == other.joystickDown
            and self.joystickLeft == other.joystickLeft
            and self.joystickRight == other.joystickRight
            and self.joystickCentre == other.joystickCentre
        )

    def __str__(self):
        return (
            f"Dials: Left={self.dialLeft}, Right={self.dialRight}\n"
            f"Buttons: {self.buttonOne}, {self.buttonTwo}, {self.buttonThree}, {self.buttonFour}, {self.buttonFive}, {self.buttonSix}\n"
            f"Joystick: Up={self.joystickUp}, Down={self.joystickDown}, Left={self.joystickLeft}, Right={self.joystickRight}, Centre={self.joystickCentre}"
        )

    def updateButtons(self, array: list):
        pass
        # self.buttonOne = array[0]
        # self.buttonTwo = array[1]
        # self.buttonThree = array[2]
        # self.buttonFour = array[3]
        # self.buttonFive = array[4]
        # self.buttonSix = array[5]
