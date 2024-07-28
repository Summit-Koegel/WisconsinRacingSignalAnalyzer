# An object for storing recieved can values
from random import randint

try:
    from can.mcpDriver import *

    can = McpCanBus()
except Exception as e:
    pass

class CombustionStruct:
    def __init__(self):
        # SPDU_FAULTS
        self._SPDU_Fault_eFuse6 = False
        self._SPDU_Fault_eFuse5 = False
        self._SPDU_Fault_eFuse4 = False
        self._SPDU_Fault_eFuse3 = False
        self._SPDU_Fault_eFuse2 = False
        self._SPDU_Fault_eFuse1 = False
        self._SPDU_Fault_AH2 = False
        self._SPDU_Fault_AH1 = False
        # PCM_HW_SENSORS_1
        self._HW_Sensors_isRealRPM = False
        self._HW_Sensors_RPM = int(0)
        self._HW_Sensors_Cyl1_MAP_Crank = int(0)
        self._HW_Sensors_Cyl1_MAP_Time = int(0)
        self._HW_Sensors_Cyl2_MAP_Crank = int(0)
        self._HW_Sensors_Cyl2_MAP_Time = int(0)
        # PCM_HW_SENSORS_2
        self._HW_Sensors_TPS1 = int(0)
        self._HW_Sensors_Cyl1_IAT = int(0)
        self._HW_Sensors_APPS1 = int(0)
        self._HW_Sensors_Cyl2_IAT = int(0)
        self._HW_Sensors_APPS2 = int(0)
        self._HW_Sensors_TPS2 = int(0)
        self._HW_Sensors_ECT = float(0.0)
        self._HW_Sensors_EOT = int(0)
        # PCM_HW_SENSORS_3
        self._HW_Sensors_SysVolt = int(0)
        self._HW_Sensors_MAF = int(0)
        self._HW_Sensors_CrankReq = False
        self._HW_Sensors_ShiftUp = False
        self._HW_Sensors_ShiftDown = False
        self._HW_Sensors_Gear = int(0)
        self._HW_Sensors_F_BrakePressure = int(0)
        self._HW_Sensors_R_BrakePressure = int(0)
        self._HW_Sensors_EStop = False
        self._HW_Sensors_TankPressure = int(0)
        self._HW_Sensors_EOP = int(0)
        # PCM_HW_SENSORS_4
        self._HW_SENSORS_Fuel_Pressure = int(0)
        self._HW_SENSORS_IAT1_FINE = int(0)
        self._HW_SENSORS_IAT2_FINE = int(0)
        self._HW_SENSORS_CAN_TC = int(0)
        self._HW_SENSORS_CAN_LC = int(0)
        # PCM_VIRTUAL_SENSORS_1
        self._Virtual_Sensors_APC = int(0)
        self._Virtual_Sensors_IMEP = int(0)
        self._Virtual_Sensors_Load = int(0)
        self._Virtual_Sensors_MAF = int(0)
        self._Virtual_Sensors_IndTorque = int(0)
        self._Virtual_Sensors_Barometric = int(0)
        self._Virtual_Sensors_MAP = int(0)
        # PCM_VIRTUAL_SENSORS_2
        self._Virtual_Sensors_APPS_Arb = int(0)
        self._Virtual_Sensors_TPS_Arb = int(0)
        self._Virtual_Sensors_IndPower = int(0)
        self._Virtual_Sensors_IndWork = int(0)
        self._Virtual_Sensors_RunTime = int(0)
        self._Virtual_Sensors_NECCT = int(0)
        # PCM_VIRTUAL_SENSORS_3
        self._Virtual_Sensors_Cyl1_UEGO = float(0.0)
        self._Virtual_Sensors_Cyl2_UEGO = float(0.0)
        self._Virtual_Sensors_Shifts_Remaining = int(0)
        self._Virtual_Sensors_EOP = int(0)
        # PCM_ENGINE_CONTROL_1
        self._Engine_Control_SOI = int(0)
        self._Engine_Control_SparkEnergy = int(0)
        self._Engine_Control_Cyl2_SparkAdv = int(0)
        self._Engine_Control_Cyl1_SparkAdv = int(0)
        # PCM_ACTUATORS_1
        self._HW_Actuators_Inj_Cyl1_InjMPW = int(0)
        self._HW_Actuators_Inj_Cyl2_InjMPW = int(0)
        self._HW_Actuators_Inj_SOI = int(0)
        self._HW_Actuators_Inj_EOI = int(0)
        self._HW_Actuators_Spark_StartAngle = int(0)
        self._HW_Actuators_CEL = False
        self._HW_Actuators_FuelPump = False
        self._HW_Actuators_Inj_InjectorsEnabled = False
        self._HW_Actuators_Shifting_ShiftDown = False
        self._HW_Actuators_Shifting_ShiftNeutral = False
        self._HW_Actuators_Shifting_ShiftUp = False
        self._HW_Actuators_Spark_SparkEnabled = False
        self._HW_Actuators_StarterSolenoidOut = False
        # PCM_ACTUATORS_2
        self._HW_Actuators_Spark_StopAngle = int(0)
        self._HW_Actuators_Spark_MaxDuration = int(0)
        self._HW_Actuators_FAN = int(0)
        self._HW_Actuators_ETC_DC = int(0)
        self._HW_Actuators_OilPump_DC = int(0)
        self._HW_Actuators_CEL = int(0)
        # PCM_ENGINE_CONTROL_2
        self._Engine_Control_Cyl1_FPC = int(0)
        self._Engine_Control_EOI = int(0)
        self._Engine_Control_ETCReq = int(0)
        self._Engine_Control_Cyl2_FPC = int(0)
        # SPDU_CURRENT_2
        self._SPDU_Current_eFuse6 = float(0)
        self._SPDU_Current_eFuse5 = float(0)
        self._SPDU_Current_eFuse4 = float(0)
        self._SPDU_Current_eFuse3 = float(0)
        # SPDU_CURRENT_1
        self._SPDU_Current_eFuse2 = float(0)
        self._SPDU_Current_eFuse1 = float(0)
        self._SPDU_Current_AH2 = float(0)
        self._SPDU_Current_AH1 = float(0)


class ElectricStruct:
    def __init__(self):
        # PCM_PerformanceFaults
        self.PCM_PF_HVactive = False
        self.PCM_PF_TractionLimited = False
        self.PCM_PF_SpinoutDetected = False
        self.PCM_PF_SlipCntlActive = False
        self.PCM_PF_PowerLimiterActive = False
        self.PCM_PF_SDC = False
        self.PCM_PF_RTD = False
        self.PCM_PF_RegenActive = False
        # BMS_Vitals
        self.Discharge_Limit = int(0)
        self.Charge_Limit = int(0)
        self.High_Cell_Temp = int(0)
        self.High_Cell_Voltage = float(0.0)
        self.Low_Cell_Voltage = float(0.0)
        self.Cell_Average_Temp = int(0)
        # IFL_FAULT_CODE
        self.IFL_SDCControl = int(0)
        self.IFL_DiagnosticInfo = int(0)
        self.IFL_FaultCode = int(0)
        # IFL_CONTROLS
        self.IFL_T_IGBT = int(0)
        self.IFL_T_winding = int(0)
        self.IFL_I_s_amplitude = int(0)
        self.IFL_P_ac = int(0)
        self.IFL_MotorSpeed = int(0)
        # IFR_FAULT_CODE
        self.IFR_SDCControl = int(0)
        self.IFR_DiagnosticInfo = int(0)
        self.IFR_FaultCode = int(0)
        # IFR_CONTROLS
        self.IFR_T_IGBT = int(0)
        self.IFR_T_winding = int(0)
        self.IFR_I_s_amplitude = int(0)
        self.IFR_P_ac = int(0)
        self.IFR_MotorSpeed = int(0)
        # IRL_FAULT_CODE
        self.IRL_SDCControl = int(0)
        self.IRL_DiagnosticInfo = int(0)
        self.IRL_FaultCode = int(0)
        # IRL_CONTROLS
        self.IRL_T_IGBT = int(0)
        self.IRL_T_winding = int(0)
        self.IRL_I_s_amplitude = int(0)
        self.IRL_P_ac = int(0)
        self.IRL_MotorSpeed = int(0)
        # IRR_FAULT_CODE
        self.IRR_SDCControl = int(0)
        self.IRR_DiagnosticInfo = int(0)
        self.IRR_FaultCode = int(0)
        # IRR_CONTROLS
        self.IRR_T_IGBT = int(0)
        self.IRR_T_winding = int(0)
        self.IRR_I_s_amplitude = int(0)
        self.IRR_P_ac = int(0)
        self.IRR_MotorSpeed = int(0)
        # Coolants_Stats
        self.DAQ_TF_CoolL = int(0)
        self.DAQ_TF_CoolR = int(0)
        self.DAQ_Temp2 = int(0)
        self.DAQ_Temp1 = int(0)
        self.DAQ_Flow2 = int(0)
        self.DAQ_Flow1 = int(0)