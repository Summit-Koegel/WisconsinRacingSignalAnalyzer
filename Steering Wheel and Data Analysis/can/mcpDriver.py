import board
import busio
import digitalio
from adafruit_bus_device.spi_device import SPIDevice

# Instructions follow the format: Read/Write, Address, Data
# Please read the data sheet for bit level mapping
BAUDRATE = 10000000

WRITE = 0x02
READ = 0x03

CAN_TX = 0x40
CAN_RX_0 = 0x90
CAN_RX_1 = 0x94
# Setting MCP mode
MCP_SET_CONFIG = bytes([0xC0])
MCP_SET_NORMAL = bytes([WRITE,0x0F,0x00])
# Config register values for 500k baud
MCP_SET_CNF1_500 = bytes([WRITE,0x2A,0xC0])
MCP_SET_CNF2_500 = bytes([WRITE,0x29,0xF0])
MCP_SET_CNF3_500 = bytes([WRITE,0x28,0x86])
# Config register values for 1000k baud
MCP_SET_CNF1_1000 = bytes([WRITE,0x2A,0xC0])
MCP_SET_CNF2_1000 = bytes([WRITE,0x29,0xD0])
MCP_SET_CNF3_1000 = bytes([WRITE,0x28,0x82])
# Setting receive filtering settings (no filtering)
MCP_SET_RXCTRL_0 = bytes([WRITE,0x60,0x60])
MCP_SET_RXCTRL_1 = bytes([WRITE,0x70,0x60])
# Obtaining the status of the MCP
MCP_READ_TX_STATUS = bytes([0xA0])
MCP_READ_RX_STATUS = bytes([0xB0])
MCP_READ_CANSTAT = bytes([READ,0x0E])

RX_START = 0x61

class McpCanBus:
    def __init__(self):
        chipSelect = digitalio.DigitalInOut(board.D25)
        self.spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
        self.mcp = SPIDevice(self.spi, chip_select=chipSelect, baudrate=BAUDRATE, polarity=0, phase=0, extra_clocks =0)

        # Reset the MCP via a spi transmission
        with self.mcp:
            self.spi.write(MCP_SET_CONFIG)
        # Set all three configuration registers
        with self.mcp:
            self.spi.write(MCP_SET_CNF1_1000)
        with self.mcp:
            self.spi.write(MCP_SET_CNF2_1000)
        with self.mcp:
            self.spi.write(MCP_SET_CNF3_1000)
        # Configure Rx Settings
        with self.mcp:
            self.spi.write(MCP_SET_RXCTRL_0)
        with self.mcp:
            self.spi.write(MCP_SET_RXCTRL_1)
        # Set MCP to operate in normal mode
        with self.mcp:
            self.spi.write(MCP_SET_NORMAL)
        
    def getStatus(self, tx):
        rxBuffer = bytearray(1)
        if tx:
            with self.mcp:
                self.spi.write(MCP_READ_TX_STATUS)
                self.spi.readinto(rxBuffer, write_value=0xFF)
        else:
            with self.mcp: 
                self.spi.write(MCP_READ_RX_STATUS)
                self.spi.readinto(rxBuffer, write_value=0xFF)

        return int.from_bytes(rxBuffer, "big")

    def checkMode(self):
        rxBuffer = bytearray(1)

        with self.mcp:
            self.spi.write(MCP_READ_CANSTAT)
            self.spi.readinto(rxBuffer, write_value=0xFF)

        return int.from_bytes(rxBuffer, "big")

    def checkRxBuffer(self):
        status = self.getStatus(False)

    def rxMessage(self):
        status = self.getStatus(False)
        # print('Status: ' + str(status) + ' Filtered: ' + str(int(status) & 0xC0))

        if ((int(status) & 0xC0) != 0x00):
            rxBuffer = bytearray(13)

            with self.mcp:
                addr = CAN_RX_0
                if ((status & 0xC0) == 0x80):
                    print('Reading 1')
                    addr = CAN_RX_1

                self.spi.write(bytes([addr]))
                self.spi.readinto(rxBuffer, write_value=0xFF)

            output = list(rxBuffer)

            extended = bool(output[3] & 0x08)

            if not extended:
                msgId = ((output[0]) << 3) | (output[1] >> 5)
            else:
                msgId = (output[0] << 19) | (output[1] << 11) | (output[2] << 8) | (output[3])

            msgLength = 0x0F & output[4]
            data = output[5:13]
        
            #print('Extended: ' + str(extended))
            #print('Id:' + str(msgId))
            #print('Length: ' + str(msgLength))
            #print(data)

            return msgId, msgLength, data

    def txMessage(self, id, length, payload, extended):
        # Ensure that the payload is the right size 
        if (len(payload) > 8):
            return False
        # Obtain the first byte returned by the status register
        status = 0x02 # (self.getStatus(True))[0]
        # Obtain the open loaction in the buffer
        txBufferAddr = int()
        if (status & 0x02):
            txBufferAddr = 0x00
        elif (status & 0x04):
            txBufferAddr = 0x02
        elif (status & 0x06):
            txBufferAddr = 0x04
        else:
            return False
        
        if (not extended):
            txID = [((id >> 3) & 0xFF),((id << 5) & 0xE0), 0x00, 0x00]
        else:
            txID = [((id >> 24) & 0xFF),((id >> 18) | (0x08) | ((id >> 16) & 0x03)),((id >> 8) & 0xFF),(id & 0xFF)]
        
        # Write value into appropriate buffer on MCP
        transmission = [((txBufferAddr | CAN_TX) & 0xFF)]
        # print(transmission)
        transmission.extend(txID)
        # print(transmission)
        transmission.extend([length & 0x07])
        # print(transmission)
        transmission.extend(payload)
        
        # print(transmission)
        # print(bytearray(transmission))
        with self.mcp:
            self.spi.write(bytes(transmission))

        with self.mcp:
            self.spi.write(bytes([0x05,0x30,0x0B,0xFF]))

