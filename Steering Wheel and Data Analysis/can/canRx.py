from can.mcpDriver import McpCanBus
import socket as sk

# IC IDs
SPDU_FAULTS = 48
PCM_HW_SENSORS_1 = 220
PCM_HW_SENSORS_2 = 221
PCM_HW_SENSORS_3 = 222
PCM_HW_SENSORS_4 = 230
PCM_HW_SENSORS_4 = 230
PCM_VIRTUAL_SENSORS_1 = 223
PCM_VIRTUAL_SENSORS_2 = 224
PCM_VIRTUAL_SENSORS_3 = 225
PCM_ENGINE_CONTROL_1 =226
PCM_ACTUATORS_1 = 227
PCM_ACTUATORS_2 = 228
PCM_ENGINE_CONTROL_2 = 229
SPDU_CURRENT_1 = 304
SPDU_CURRENT_2 = 305
EVO_GPS = 50
# EV IDs
BMS_VITALS = 161
IFL_FAULT_CODE = 209
IFL_CONTROLS = 196
IFR_FAULT_CODE = 208
IFR_CONTROLS = 192
IRL_FAULT_CODE = 210
IRL_CONTROLS = 200
IRR_FAULT_CODE = 211
IRR_CONTROLS = 204
COOLANT_STATS = 2
    

def rxIcCANmsgs(mcp, struct, transmitter):
    try:
        id, length, payload = mcp.rxMessage()
        #print('ID: ' + str(id))
    except:
        id = 0
        length = 0

    if (id == SPDU_FAULTS and length == 1):
        struct._SPDU_Fault_eFuse6 = True if ((payload[0] >> 7) & 0x01) else False
        struct._SPDU_Fault_eFuse5 = True if ((payload[0] >> 6) & 0x01) else False
        struct._SPDU_Fault_eFuse4 = True if ((payload[0] >> 5) & 0x01) else False
        struct._SPDU_Fault_eFuse3 = True if ((payload[0] >> 4) & 0x01) else False
        struct._SPDU_Fault_eFuse2 = True if ((payload[0] >> 3) & 0x01) else False
        struct._SPDU_Fault_eFuse1 = True if ((payload[0] >> 2) & 0x01) else False
        struct._SPDU_Fault_AH2 =    True if ((payload[0] >> 1) & 0x01) else False
        struct._SPDU_Fault_AH1 =    True if ((payload[0]) & 0x01) else False
        print('SPDU_FAULTS')
    
    elif (id == PCM_HW_SENSORS_1 and length == 8):
        struct._HW_Sensors_isRealRPM =      payload[7] & 0x01
        struct._HW_Sensors_RPM =           (payload[4] << 8) | payload[5]
        struct._HW_Sensors_Cyl1_MAP_Crank = payload[0]
        struct._HW_Sensors_Cyl1_MAP_Time =  payload[1]
        struct._HW_Sensors_Cyl2_MAP_Crank = payload[2]
        struct._HW_Sensors_Cyl2_MAP_Time =  payload[3]
        struct._HW_Sensors_FuelPressure =   payload[6]
        #print('HW_SENSORS_1')

    elif (id == PCM_HW_SENSORS_2 and length == 8):
        struct._HW_Sensors_APPS1 =    payload[0]
        struct._HW_Sensors_APPS2 =    payload[1]
        struct._HW_Sensors_TPS1 =     payload[2]
        struct._HW_Sensors_TPS2 =     payload[3]
        struct._HW_Sensors_Cyl2_IAT = payload[4]
        struct._HW_Sensors_Cyl1_IAT = payload[5]
        struct._HW_Sensors_ECT =      payload[6] / 100.0
        struct._HW_Sensors_EOT =      payload[7]
        print('HW_SENSORS_2')

    elif (id == PCM_HW_SENSORS_3 and length == 8):
        struct._HW_Sensors_SysVolt =           ((payload[0] << 8) | payload[1]) / 10.0
        struct._HW_Sensors_MAF =                 payload[2]
        struct._HW_Sensors_R_BrakePressure =     payload[3]
        struct._HW_Sensors_F_BrakePressure =     payload[4]
        struct._HW_Sensors_Gear =                payload[5] & 0x07
        struct._HW_Sensors_EStop =     True if ((payload[5] >> 3) & 0x01) else False
        struct._HW_Sensors_CrankReq =  True if ((payload[5] >> 4) & 0x01) else False
        struct._HW_Sensors_ShiftUp =   True if ((payload[5] >> 5) & 0x01) else False
        struct._HW_Sensors_ShiftDown = True if ((payload[5] >> 6) & 0x01) else False
        struct._HW_Sensors_TankPressure =        payload[6]
        struct._HW_Sensors_EOP =                 payload[7]
        #print('HW_SENSORS_3')

    elif (id == PCM_HW_SENSORS_4 and length == 8):
        struct._HW_SENSORS_FUEL_PRESSURE = (payload[0] << 8) | payload[1] 
        struct._HW_SENSORS_IAT1_FINE =     (payload[2] << 8) | payload[3]
        struct._HW_SENSORS_IAT2_FINE =     (payload[4] << 8) | payload[5]
        struct._HW_SENSORS_CAN_TC =         payload[6]
        struct._HW_SENSORS_CAN_LC =         payload[7]
        print('HW_SENSORS_4')

    elif (id == PCM_VIRTUAL_SENSORS_1 and length == 8):
        struct._Virtual_Sensors_Barometric = payload[0]
        struct._Virtual_Sensors_MAP =        payload[1]
        struct._Virtual_Sensors_MAF =       (payload[2] << 8) | payload[3]
        struct._Virtual_Sensors_APC =        payload[4]
        struct._Virtual_Sensors_IndTorque =  payload[5]
        struct._Virtual_Sensors_IMEP =       payload[6]
        struct._Virtual_Sensors_Load =       payload[7]
        print('PCM_VIRTUAL_SENSORS_1')

    elif (id == PCM_VIRTUAL_SENSORS_2 and length == 8):
        struct._Virtual_Sensors_IndPower =  payload[0]
        struct._Virtual_Sensors_IndWork =   payload[1]
        struct._Virtual_Sensors_NECCT =     payload[2]
        struct._Virtual_Sensors_RunTime =   payload[3]
        struct._Virtual_Sensors_TPS_Arb =  (payload[4] << 8) | payload[5]
        struct._Virtual_Sensors_APPS_Arb = (payload[6] << 8) | payload[7]
        print('PCM_VIRTUAL_SENSORS_2')

    elif (id == PCM_VIRTUAL_SENSORS_3 and length == 8):
        struct._Virtual_Sensors_Cyl1_UEGO =          payload[0]
        struct._Virtual_Sensors_Cyl2_UEGO =          payload[1]
        struct._Virtual_Sensors_Shifts_Remaining =   (payload[2] << 8) | payload[3] # Dont use anything other than multiples of 8 please
        struct._Virtual_Sensors_EOP =                (payload[4] << 8) | payload[5] # I don't have the time to transcribe those
        #print('PCM_VIRTUAL_SENSORS_3')

    elif (id == PCM_ENGINE_CONTROL_1 and length == 8):
        struct._Engine_Control_Cyl2_SparkAdv = (payload[0] << 8) | payload[1]
        struct._Engine_Control_SOI =           (payload[2] << 8) | payload[3]
        struct._Engine_Control_SparkEnergy =   (payload[4] << 8) | payload[5]
        struct._Engine_Control_Cyl1_SparkAdv = (payload[6] << 8) | payload[7]
        #print('PCM_ENGINE_CONTROL_1')

    elif (id == PCM_ACTUATORS_1 and length == 8):
        struct._HW_Actuators_Inj_Cyl1_InjMPW =                (payload[0] << 8) | payload[1]
        struct._HW_Actuators_Inj_Cyl2_InjMPW =                (payload[2] << 8) | payload[3]
        struct._HW_Actuators_Inj_SOI =                         payload[4]
        struct._HW_Actuators_Inj_EOI =                         payload[5]
        struct._HW_Actuators_Spark_StartAngle =       True if (payload[6] & 0x01) else False
        struct._HW_Actuators_CEL =                   True if ((payload[6] >> 1) & 0x01) else False
        struct._HW_Actuators_FuelPump =              True if ((payload[6] >> 2) & 0x01) else False
        struct._HW_Actuators_Inj_InjectorsEnabled =  True if ((payload[6] >> 3) & 0x01) else False
        struct._HW_Actuators_Shifting_ShiftDown =    True if ((payload[6] >> 4) & 0x01) else False
        struct._HW_Actuators_Shifting_ShiftNeutral = True if ((payload[6] >> 5) & 0x01) else False
        struct._HW_Actuators_Shifting_ShiftUp =      True if ((payload[6] >> 6) & 0x01) else False
        struct._HW_Actuators_Spark_SparkEnabled =    True if ((payload[6] >> 7) & 0x01) else False
        struct._HW_Actuators_StarterSolenoidOut =    True if (payload[7] & 0x01) else False
        #print('PCM_ACTUATORS_1')

    elif (id == PCM_ACTUATORS_2 and length == 8):
        struct._HW_Actuators_ETC_DC =           (payload[0] << 8) | payload[1]
        struct._HW_Actuators_OilPump_DC =        payload[2]
        struct._HW_Actuators_Spark_MaxDuration = payload[3]
        struct._HW_Actuators_Spark_StopAngle =   payload[4]
        struct._HW_Actuators_FAN =      True if (payload[5] & 0x1F) else False
        struct._HW_Actuators_CEL =              (payload[5] << 3) | (payload[6] >> 5)
        print('PCM_ACTUATORS_2')

    elif (id == PCM_ENGINE_CONTROL_2 and length == 8):
        struct._Engine_Control_Cyl2_FPC = (payload[0] << 8) | payload[1]
        struct._Engine_Control_ETCReq =   (payload[2] << 8) | payload[3]
        struct._Engine_Control_EOI =      (payload[4] << 8) | payload[5]
        struct._Engine_Control_Cyl1_FPC = (payload[6] << 8) | payload[7]
        #print('PCM_ENGINE_CONTROL_2')

    elif (id == SPDU_CURRENT_2 and length == 8):
        struct._SPDU_Current_eFuse3 = (payload[0] << 8) | payload[1]
        struct._SPDU_Current_eFuse4 = (payload[2] << 8) | payload[3]
        struct._SPDU_Current_eFuse5 = (payload[4] << 8) | payload[5]
        struct._SPDU_Current_eFuse6 = (payload[6] << 8) | payload[7]
        print('SPDU_CURRENT_2')

    elif (id == SPDU_CURRENT_1 and length == 8):
        struct._SPDU_Current_AH1 =    (payload[0] << 8) | payload[1]
        struct._SPDU_Current_AH2 =    (payload[2] << 8) | payload[3]
        struct._SPDU_Current_eFuse1 = (payload[4] << 8) | payload[5]
        struct._SPDU_Current_eFuse2 = (payload[6] << 8) | payload[7]
        print('SPDU_CURRENT_1')

    elif (id != 0):
        print('Unexpected Message:: ID: ' + str(id) + ', Len: ' + str(length))

    if ((id != 0) and (transmitter != None)):
        try:
            # Send CAN message to Can Server
            addr = ('10.141.121.100', 4096)
            inet_payload = (id).to_bytes(4, "big") + (length).to_bytes(1, "big") + bytes(payload)
            # Send Request
            transmitter.sendto(inet_payload, addr)
        except:
            None

def rxEvCANmsgs(mcp, struct, transmitter):
    try:
        id, length, payload = mcp.rxMessage()
    except:
        id = 0
        length = 0
    
    if (id == BMS_VITALS and length == 8):
        print(str(payload))
        struct.Discharge_Limit = (payload[7] << 8) | payload[6]
        struct.Charge_Limit = payload[4]
        struct.High_Cell_Temp = payload[3]
        struct.High_Cell_Voltage = float(payload[2]) / 10.0
        struct.Low_Cell_Voltage = float(payload[1]) / 10.0
        struct.Cell_Average_Temp = payload[0]
        print('BMS Vitals - DL: ' + str(struct.Discharge_Limit) + ', CL: ' + str(struct.Charge_Limit) 
              + ', HCT: ' + str(struct.High_Cell_Temp) + ', HCV: ' + str(struct.High_Cell_Voltage) 
              + ', LCV: ' + str(struct.Low_Cell_Voltage) + ', CAT: '  + str(struct.Cell_Average_Temp))
    
    elif (id == IFL_FAULT_CODE and length == 5):
        struct.IFL_SDCControl = payload[5]
        struct.IFL_DiagnosticInfo = (payload[3] << 8) | payload[2]
        struct.IFL_FaultCode = (payload[1] << 8) | payload[0]
    
    elif (id == IFL_CONTROLS and length == 8):
        struct.IFL_T_IGBT = payload[7]
        struct.IFL_T_winding = payload[6]
        struct.IFL_I_s_amplitude = (payload[5] << 8) | payload[4]
        struct.IFL_P_ac = (payload[3] << 8) | payload[2]
        struct.IFL_MotorSpeed = (payload[1] << 8) | payload[0]
     
    elif (id == IFR_FAULT_CODE and length == 5):
        struct.IFR_SDCControl = payload[5]
        struct.IFR_DiagnosticInfo = (payload[3] << 8) | payload[2]
        struct.IFR_FaultCode = (payload[1] << 8) | payload[0]
     
    elif (id == IFR_CONTROLS and length == 8):
        struct.IFR_T_IGBT = payload[7]
        struct.IFR_T_winding = payload[6]
        struct.IFR_I_s_amplitude = (payload[5] << 8) | payload[4]
        struct.IFR_P_ac = (payload[3] << 8) | payload[2]
        struct.IFR_MotorSpeed = (payload[1] << 8) | payload[0]
     
    elif (id == IRL_FAULT_CODE and length == 5):
        struct.IRL_SDCControl = payload[5]
        struct.IRL_DiagnosticInfo = (payload[3] << 8) | payload[2]
        struct.IRL_FaultCode = (payload[1] << 8) | payload[0]
     
    elif (id == IRL_CONTROLS and length == 8):
        #print(str(payload))
        struct.IRL_T_IGBT = float(payload[7]) - 40
        struct.IRL_T_winding = float(payload[6]) - 40
        struct.IRL_I_s_amplitude = float((payload[5] << 8) | payload[4]) / 0.02
        struct.IRL_P_ac = float((payload[3] << 8) | payload[2]) / 2
        struct.IRL_MotorSpeed = (payload[1] << 8) | payload[0]
        #print('IRL CONTROLS - T_IGBT: ' + str(struct.IRL_T_IGBT) + ', T_WIND: ' 
              #+ str(struct.IRL_T_winding) + ', Is: ' + str(struct.IRL_I_s_amplitude) 
              #+ ',Pac: ' + str(struct.IRL_P_ac) + ', RPM: ' + str(struct.IRL_MotorSpeed))
     
    elif (id == IRR_FAULT_CODE and length == 5):
        struct.IRR_SDCControl = payload[5]
        struct.IRR_DiagnosticInfo = (payload[3] << 8) | payload[2]
        struct.IRR_FaultCode = (payload[1] << 8) | payload[0]
     
    elif (id == IRR_CONTROLS and length == 8):
        #print(str(payload))
        struct.IRR_T_IGBT = float(payload[7]) - 40
        struct.IRR_T_winding = float(payload[6]) - 40
        struct.IRR_I_s_amplitude = float((payload[5] << 8) | payload[4]) / 0.02
        struct.IRR_P_ac = float((payload[3] << 8) | payload[2]) / 2
        struct.IRR_MotorSpeed = (payload[1] << 8) | payload[0]
        #print('IRR CONTROLS - T_IGBT: ' + str(struct.IRR_T_IGBT) + ', T_WIND: ' 
              #+ str(struct.IRR_T_winding) + ', Is: ' + str(struct.IRR_I_s_amplitude) 
              #+ ',Pac: ' + str(struct.IRR_P_ac) + ', RPM: ' + str(struct.IRR_MotorSpeed))
    
    elif (id == COOLANT_STATS and  length == 8):
        struct.DAQ_TF_CoolL = payload[5]
        struct.DAQ_TF_CoolR = payload[4]
        struct.DAQ_Temp2 = payload[3]
        struct.DAQ_Temp1 = payload[2]
        struct.DAQ_Flow2 = payload[1]
        struct.DAQ_Flow1 = payload[0]

    else:
        None
        # print('Unexpexted ID/Length - ID: ' + str(id) + ', Length: ' + str(length))

    if ((id != 0)):
        try:
            # Send CAN message to Can Server
            addr = ('255.255.255.255', 1313)
            inet_payload = (id).to_bytes(4, "big") + (length).to_bytes(1, "big") + bytes(payload)
            # Send Request
            (sk.socket(sk.AF_INET, sk.SOCK_DGRAM)).sendto(inet_payload, addr)
        except:
            None