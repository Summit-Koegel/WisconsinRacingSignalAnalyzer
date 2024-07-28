class InputDevice:
    def __init__(self):
        self.callback = None
        self.args = []
        self.kwargs = {}
    
    def register_callback(self, callback, *args, **kwargs):
        self.callback = callback
        self.args = args
        self.kwargs = kwargs

    def run_callback(self):
        if self.callback:
            self.callback(*self.args, **self.kwargs)
        else:
            print("No callback function registered")

class Dial(InputDevice):
    def __init__(self, dial_name):
        super().__init__()
        self.dial_name = dial_name

    def turn(self):
        print(f'{self.dial_name} dial turned')
        self.activate()