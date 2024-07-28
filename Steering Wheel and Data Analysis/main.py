 #!/usr/bin/env python3

DEBUG = True
ON_PI = False

if(DEBUG): print("Starting Steering Wheel as:")

if(DEBUG): print("Importing multiprocessing")
import multiprocessing   as mp
if ON_PI:
    if(DEBUG): print("Importing CAN functions")
    import can.canSM         as csm
    if(DEBUG): print("Importing GPIO functions")
    import gpio.gpioSM       as ism
if(DEBUG): print("Importing Display functions")
import display.displaySM as dsm
import os

def __main__():
    # Init the state machines for each process
    print("Starting State machines")

    # Prepare pipes for multiprocessing data transfer
    print("Preparing pipes for usage")
    # Format of Source, Pipe, Destination
    canPipeDisplay = mp.SimpleQueue()
    canPipeIo = mp.SimpleQueue()
    ioPipeCAN = mp.SimpleQueue()
    ioPipeDisplay = mp.SimpleQueue()

    # Endless processing loop
    if ON_PI:
        canProcess = mp.Process(target=processCAN, args=(canPipeDisplay, canPipeIo, ioPipeCAN,))
        ioProcess = mp.Process(target=processGPIO, args=(canPipeIo, ioPipeCAN,ioPipeDisplay,))
    displayProcess = mp.Process(target=processDisplay, args=(canPipeDisplay,ioPipeDisplay))

    # Fork the display off
    print("forking display off")
    displayProcess.start()
    displayProcess.join()
    if ON_PI:
        canProcess.start()
        ioProcess.start()

# Utilize the CAN state machine to run all things CAN
def processCAN(canPipeDisplay, canPipeIo, ioPipeCAN):
    csm.runCAN(canPipeDisplay, canPipeIo, ioPipeCAN)

# Utilize the GPIO state machine to run all things GPIO
def processGPIO(canPipeIo, ioPipeCAN, ioPipeDisplay):
    ism.runGPIO(canPipeIo, ioPipeCAN, ioPipeDisplay)

# Utilize the display state machine to run all the screen realted items
def processDisplay(canPipe, ioPipeDisplay):
    dsm.runDisplay(canPipe, ioPipeDisplay)

# Run main
if __name__ == '__main__':
    __main__()