from ctypes import *
import ctypes
from bitflag import BitFlag

BAL_MAX_CNT_CELLS = 16


class ParamsBmsCfg(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        # cooling
        ('TempCoolingStart', c_int8),        # xx C 52
        ('TempCoolingStop',  c_int8),        # xx C 45
        # heating
        ('TempHeatingStart', c_int8),       # xx �C 2
        ('TempHeatingStop', c_int8),       # xx �C 5
        ('VChargeHeatingLowerLimit', c_uint16),  # mV
        # cell
        ('VCellLowLimit',      c_uint16),   # x.xx     int = V x 62.52
        ('VCellLowLimitReset', c_uint16),   # x.xx V
        ('VCellHighLimit',     c_uint16),   # x.xx V
        ('VCellHighLimitReset', c_uint16),   # x.xx V
        ('CountCells',         c_uint8),    # xx
        # battery
        ('VBatHighLimit',      c_uint16),   # xx.x V
        ('VBatHighLimitReset', c_uint16),   # xx.x V
        ('VBatLowLimit',       c_uint16),   # xx.x V
        ('VBatLowLimitReset',  c_uint16),   # xx.x V
        # balancing
        ('VCellMaxDeviation',      c_uint16),  # x.xx V
        ('VCellMinDeviation',      c_uint16),
        ('VCellBalanceHighLimit',  c_uint16),  # x.xx   V
        ('VCellBalanceLowLimit',   c_uint16),  # x.xx   V
        ('TempLowLimitBalancing',  c_int8),
        ('VBatLowLimitBalancing',    c_uint16),
        ('CurrentChargeBalLimit',    c_uint16),
        ('CurrentDischargeBalLimit', c_uint16),
        ('BalCurrentHighlimit', c_uint8),     # balancing current in 25 mA limitation
        ('BalMaxPeriodInSec',   c_uint8),   # max balancing period between two cells
        # charging
        ('TempLowLimitCharge',      c_int8),   # xx �C 2
        ('TempLowLimitChargeReset', c_int8),   # xx �C 3
        ('TempHighLimitCharge',     c_int8),   # xx C
        ('TempHighLimitChargeReset', c_int8),   # xx C
        ('ChargeCurrentLimit',      c_int16),  # xxx  �A  Int = (A/.8) + 512
        # discharging
        ('TempLowLimitDischarge',       c_int8),  # xx �C -20
        ('TempLowLimitDischargeReset',  c_int8),  # xx �C -15
        ('TempHighLimitDischarge',      c_int8),  # xx C
        ('TempHighLimitDischargeReset', c_int8),  # xx C
        ('DischargeCurrentLimit',       c_int16),  # xxx  A, negative
        ('VDischargeOutsideLowLimit',   c_uint16),  # xxx  A, negative
        # SOC
        ('InitialSOC', c_uint8),   # xx %
        ('CellAh', c_uint8),  # xxxx AH
        ('VEmptyCell', c_uint16),
        ('VFullCell', c_uint16),
        ('VEmptyBattery', c_uint16),
        ('VFullBattery', c_uint16),
        # under/over voltage
        ('VDischargeOutsideHighLimit', c_uint16),  # xx.x V
        ('VChargeOutsideLowLimit',     c_uint16),  # xx.x V
        # Charge/Discharge contactors type
        ('ContType', c_uint8),  # LATCH/NON LATCH
        # ACP
        ('ACPLowLimit', c_uint16),  # xx.x V
        ('ACPLowLimitReset', c_uint16),  # xx.x V
        # Charge+Discharge contactors
        ('TiedBothOpenDelaySec', c_uint16),   #
        ('TiedBothOpenTries', c_uint8),       #
        # AGM
        ('VAGMLowLimit', c_uint16),
        # Coarse Current Sensor
        ('MeasCoarseCurSensScale', c_uint16),
        ('DefaultCoarseCurSensScale', c_uint16),
        ]

    def printing(self):
        head = 5*"-" + " ParamsBmsCfg " + 5*"-"
        print(head)
        for field in self._fields_:
            print("%s : 0x%02x" % (field[0], getattr(self, field[0])))
        print(len(head)*"-")

    def to_dict(self):
        dictOut = {}
        for field in self._fields_:
            dictOut[field[0]] = getattr(self, field[0])
        return dictOut

    def from_dict(self, dataDict: dict = {}):
        for field in self._fields_:
            field_name = field[0]
            setattr(self, field_name, dataDict[field_name])

class Flags_bits(ctypes.LittleEndianStructure):
    _fields_ = [
        ("vbat_high",  c_uint32, 1),
        ("vbat_low",  c_uint32, 1),
        ("vcell_high",  c_uint32, 1),
        ("vcell_low",  c_uint32, 1),
        ("discharge_overcurrent",  c_uint32, 1),
        ("charge_overcurrent",  c_uint32, 1),
        ("temp_high",  c_uint32, 1),
        ("temp_charge_low",  c_uint32, 1),
        ("temp_discharge_low",  c_uint32, 1),
        ("heat_required",  c_uint32, 1),
        ("cool_required",  c_uint32, 1),
        ("heat_close",  c_uint32, 1),
        ("cool_close",  c_uint32, 1),
        ("tied_together",  c_uint32, 1),
        ("critical_deviation",  c_uint32, 1),
        ("over_voltage_discharge",  c_uint32, 1),
        ("under_voltage_charge",  c_uint32, 1),
        ("reset_required",  c_uint32, 1),
        ("force_charge_open",  c_uint32, 1),
        ("force_discharge_open",  c_uint32, 1),
        ("charge_close",  c_uint32, 1),
        ("discharge_close",  c_uint32, 1),
        ("charge_sense",  c_uint32, 1),
        ("discharge_sense",  c_uint32, 1),
        ("balancer_close",  c_uint32, 1),
        ("balancing_enable",  c_uint32, 1),
        ("force_ch_enable",  c_uint32, 1),
        ("temp_discharge_high",  c_uint32, 1),
        ("reserved_28_31",  c_uint32, 4)
    ]


def get_bitflags(init_val:int = None):
    flag_names = []
    for flag in Flags_bits._fields_:
        flag_names.append(flag[0].upper())

    flags = BitFlag(
        "%s" % flag_names[0],
        "%s" % flag_names[1],
        "%s" % flag_names[2],
        "%s" % flag_names[3],
        "%s" % flag_names[4],
        "%s" % flag_names[5],
        "%s" % flag_names[6],
        "%s" % flag_names[7],
        "%s" % flag_names[8],
        "%s" % flag_names[9],
        "%s" % flag_names[10],
        "%s" % flag_names[11],
        "%s" % flag_names[12],
        "%s" % flag_names[13],
        "%s" % flag_names[14],
        "%s" % flag_names[15],
        "%s" % flag_names[16],
        "%s" % flag_names[17],
        "%s" % flag_names[18],
        "%s" % flag_names[19],
        "%s" % flag_names[20],
        "%s" % flag_names[21],
        "%s" % flag_names[22],
        "%s" % flag_names[23],
        "%s" % flag_names[24],
        "%s" % flag_names[25],
        "%s" % flag_names[26],
        "%s" % flag_names[27],
    )
    if init_val:
        flags.flags = init_val
    return flags


class Flags(ctypes.Union):
    _fields_ = [
        ("fields", Flags_bits),
        ("d32", c_uint32)  # Note: fix for x64 Dll build
    ]


class BmsSystemStatus(ctypes.Structure):
    _pack_ = 1
    _fields_ = [
        ('utime', c_uint32),  # Unix timestamp
        ('VCell', c_uint16 * BAL_MAX_CNT_CELLS),  # Cell voltages, mV
        ('TCell', c_int8 * BAL_MAX_CNT_CELLS),  # Cell temperatures, Celcius
        ('Current', c_int16),  # Battery current, A
        ('fineCurrent', c_int32), # Fine current, mA
        ('VContactorCharge', c_uint16),  # Voltage on the CH  contactor, mV
        ('VContactorDischarge', c_uint16),  # Voltage on the DCH contactor, mV
        ('VBatt', c_uint16),  # Battery voltage, mV
        ('SOC', c_uint8),  # State of charge
        ('TContactorCharge', c_int8),  # temperature, Celcius
        ('TContactorDischarge', c_int8),  # temperature, Celcius
        ('Taux1', c_int8),  # temperature, Celcius
        ('Taux2', c_int8),  # temperature, Celcius
        ('balSrcCell', c_uint8),  # source cell in balancing process with high voltage
        ('balSinkCell', c_uint8),  # sink cell in balancing process with low voltage
        ('balMode', c_uint8),  # auto - 0, manual - 1 (BMS drives balancing process)
        ('balCurrent', c_uint8),# balancing current in 25 mA units
        ('flags', Flags)  # BMS status, bit-coded, hexadecimal
    ]


class BmsInfo(ctypes.Structure):
    _fields_ = [
        ('major', c_uint32),
        ('minor', c_uint32)
    ]
