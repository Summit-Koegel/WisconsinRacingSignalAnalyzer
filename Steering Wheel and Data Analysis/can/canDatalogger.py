import queue
import threading
import time
import csv

from canStruct import CombustionStruct, ElectricStruct
from can.mcpDriver import McpCanBus

can_data = None

can_message_queue = queue.Queue()
csv_file_path = "canDatalogger.csv"

# Thread function for receiving and logging CAN messages
def receive_and_log_messages(can, struct):
    global can_data
    while True:
        msg = can.rxMessage()  # Receive a CAN message
        if msg:
            if can_data:
                if can_data.EV_MODE:
                    # Process Electric messages
                    id, length, data = msg
                    # TODO Logic for specific EV messages
                    if id == 0x100:
                        can_data.struct.PCM_PF_HVactive = bool(data[0] & 0x01)
                        can_data.struct.PCM_PF_TractionLimited = bool(data[0] & 0x02)

                else:
                    # Process Combustion messages
                    id, length, data = msg
                    # TODO Logic for specific CV messages
                    if id == 0x200:
                        can_data.struct._SPDU_Fault_eFuse6 = bool(data[0] & 0x01)
                        can_data.struct._SPDU_Fault_eFuse5 = bool(data[0] & 0x02)

            can_message_queue.put(msg)

        # This is where we need to call the to_dict function from canStruct
        # and write that dictionary to the csvfile
        # with open(csv_file_path, 'w', newline='') as csvfile:
        #     fieldnames = data_dict.keys()
        #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        #     writer.writeheader()

        #     writer.writerow(data_dict)

# Write all the data from canStruct variables to a dict

# Create and start a thread for receiving and logging CAN messages
def start_can_thread():
    can = McpCanBus()
    global can_data
    can_data = canStateMachine()
    threading.Thread(target=receive_and_log_messages, args=(can,), daemon=True).start()

# Function to get the latest CAN messages from the queue
def get_latest_can_messages():
    messages = []
    while not can_message_queue.empty():
        messages.append(can_message_queue.get())
    return messages

if __name__ == '__main__':
    start_can_thread()

    while True:
        time.sleep(1)
        latest_messages = get_latest_can_messages()
        if latest_messages:
            print("Received CAN Messages:")
            for msg in latest_messages:
                print(msg)
