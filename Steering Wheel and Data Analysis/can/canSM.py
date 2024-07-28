import csv
DEBUG = True

from time import sleep
import socket as sk

if(DEBUG): print("   Importing MCP Driver")
from can.mcpDriver  import *
if(DEBUG): print("   Importing CAN struct")
from can.canStruct import *
if(DEBUG): print("   Importing CAN Rx")
from can.canRx     import *
if(DEBUG): print("   Importing CAN Tx")
# from can.canTx     import *
if(DEBUG): print("   Importing IO Struct")
from gpio.ioStruct import *

HEADER_LENGTH = 9
MAX_LENGTH = 5000

EV_MODE = False

# A state machine for controlling can transmissions and reciepts
class canStateMachine:
    def __init__(self):
        # self.can = McpCanBus()
        if EV_MODE:
            self.struct = ElectricStruct()
        else:
            self.struct = CombustionStruct()

        # self.ioData = IoStruct()
        # try:
        #     self.server = sk.socket(sk.AF_INET, sk.SOCK_DGRAM)
        #     addr = ('0.0.0.0', 2048)
        #     self.server.bind(addr)
        #     self.server.setblocking(False)
        #     print('Socket opened on IP: ' + addr[0] + ' Port: ' + str(addr[1]))
        # except:
        #     None

    def readIo(self, ioPipe):
        while (not(ioPipe.empty())):
            # Harvest io
            self.ioData = ioPipe.get()


def runCAN(canPipeDisplay, canPipeIo, ioPipeCan):
    pass
    canSM = canStateMachine()
    canSM.transmitter = None

    while (True):
        if EV_MODE:
            rxEvCANmsgs(can, canSM.struct, canSM.transmitter)
        else:
            rxIcCANmsgs(can, canSM.struct, canSM.transmitter)

        canPipeDisplay.put(canSM.struct)
        canPipeIo.put(canSM.struct)

        canSM.readIo(ioPipeCan)

        dictData = to_dict(canSM.struct)

        with open("canDatalogger.csv", 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile)
            
            # Write a single row of data
            writer.writerow(dictData)

        #try:
            #payload, addr = canSM.server.recvfrom(HEADER_LENGTH + MAX_LENGTH)

            #print('Message Rx over inet')
            #if(not(addr is None)):
                #msgId = int.from_bytes([payload[0], payload[1], payload[2], payload[3]], "big")
                #msgLen = int.from_bytes([payload[4]], "big")

                #msgPayload = (payload[5:])

                #canSM.can.txMessage(msgId, msgLen, msgPayload, False)
        #except:
            #addr = None

def to_dict(struct):
    return {attr: getattr(struct, attr) for attr in vars(struct)}
