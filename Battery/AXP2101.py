'''
@license MIT License

Copyright (c) 2022 lewis he

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

@file      AXP2101.py
@author    Lewis He (lewishe@outlook.com)
@date      2022-10-20

'''

from I2CInterface import *


_AXP2101_STATUS1 = const(0x00)
_AXP2101_STATUS2 = const(0x01)
_AXP2101_IC_TYPE = const(0x03)
_AXP2101_DATA_BUFFER1 = const(0x04)
_AXP2101_DATA_BUFFER2 = const(0x05)
_AXP2101_DATA_BUFFER3 = const(0x06)
_AXP2101_DATA_BUFFER4 = const(0x07)
_AXP2101_DATA_BUFFER_SIZE = const(4)
_AXP2101_COMMON_CONFIG = const(0x10)
_AXP2101_BATFET_CTRL = const(0x12)
_AXP2101_DIE_TEMP_CTRL = const(0x13)
_AXP2101_MIN_SYS_VOL_CTRL = const(0x14)
_AXP2101_INPUT_VOL_LIMIT_CTRL = const(0x15)
_AXP2101_INPUT_CUR_LIMIT_CTRL = const(0x16)
_AXP2101_RESET_FUEL_GAUGE = const(0x17)
_AXP2101_CHARGE_GAUGE_WDT_CTRL = const(0x18)
_AXP2101_WDT_CTRL = const(0x19)
_AXP2101_LOW_BAT_WARN_SET = const(0x1A)
_AXP2101_PWRON_STATUS = const(0x20)
_AXP2101_PWROFF_STATUS = const(0x21)
_AXP2101_PWROFF_EN = const(0x22)
_AXP2101_DC_OVP_UVP_CTRL = const(0x23)
_AXP2101_VOFF_SET = const(0x24)
_AXP2101_PWROK_SEQU_CTRL = const(0x25)
_AXP2101_SLEEP_WAKEUP_CTRL = const(0x26)
_AXP2101_IRQ_OFF_ON_LEVEL_CTRL = const(0x27)
_AXP2101_FAST_PWRON_SET0 = const(0x28)
_AXP2101_FAST_PWRON_SET1 = const(0x29)
_AXP2101_FAST_PWRON_SET2 = const(0x2A)
_AXP2101_FAST_PWRON_CTRL = const(0x2B)
_AXP2101_ADC_CHANNEL_CTRL = const(0x30)
_AXP2101_ADC_DATA_RELUST0 = const(0x34)
_AXP2101_ADC_DATA_RELUST1 = const(0x35)
_AXP2101_ADC_DATA_RELUST2 = const(0x36)
_AXP2101_ADC_DATA_RELUST3 = const(0x37)
_AXP2101_ADC_DATA_RELUST4 = const(0x38)
_AXP2101_ADC_DATA_RELUST5 = const(0x39)
_AXP2101_ADC_DATA_RELUST6 = const(0x3A)
_AXP2101_ADC_DATA_RELUST7 = const(0x3B)
_AXP2101_ADC_DATA_RELUST8 = const(0x3C)
_AXP2101_ADC_DATA_RELUST9 = const(0x3D)
# INTERRUPT REGISTER
_AXP2101_INTEN1 = const(0x40)
_AXP2101_INTEN2 = const(0x41)
_AXP2101_INTEN3 = const(0x42)
# INTERRUPT STATUS REGISTER
_AXP2101_INTSTS1 = const(0x48)
_AXP2101_INTSTS2 = const(0x49)
_AXP2101_INTSTS3 = const(0x4A)
_AXP2101_INTSTS_CNT = const(3)
_AXP2101_TS_PIN_CTRL = const(0x50)
_AXP2101_TS_HYSL2H_SET = const(0x52)
_AXP2101_TS_LYSL2H_SET = const(0x53)
_AXP2101_VLTF_CHG_SET = const(0x54)
_AXP2101_VHLTF_CHG_SET = const(0x55)
_AXP2101_VLTF_WORK_SET = const(0x56)
_AXP2101_VHLTF_WORK_SET = const(0x57)
_AXP2101_JIETA_EN_CTRL = const(0x58)
_AXP2101_JIETA_SET0 = const(0x59)
_AXP2101_JIETA_SET1 = const(0x5A)
_AXP2101_JIETA_SET2 = const(0x5B)
_AXP2101_IPRECHG_SET = const(0x61)
_AXP2101_ICC_CHG_SET = const(0x62)
_AXP2101_ITERM_CHG_SET_CTRL = const(0x63)
_AXP2101_CV_CHG_VOL_SET = const(0x64)
_AXP2101_THE_REGU_THRES_SET = const(0x65)
_AXP2101_CHG_TIMEOUT_SET_CTRL = const(0x67)
_AXP2101_BAT_DET_CTRL = const(0x68)
_AXP2101_CHGLED_SET_CTRL = const(0x69)
_AXP2101_BTN_VOL_MIN = const(2600)
_AXP2101_BTN_VOL_MAX = const(3300)
_AXP2101_BTN_VOL_STEPS = const(100)
_AXP2101_BTN_BAT_CHG_VOL_SET = const(0x6A)
_AXP2101_DC_ONOFF_DVM_CTRL = const(0x80)
_AXP2101_DC_FORCE_PWM_CTRL = const(0x81)
_AXP2101_DC_VOL0_CTRL = const(0x82)
_AXP2101_DC_VOL1_CTRL = const(0x83)
_AXP2101_DC_VOL2_CTRL = const(0x84)
_AXP2101_DC_VOL3_CTRL = const(0x85)
_AXP2101_DC_VOL4_CTRL = const(0x86)
_AXP2101_LDO_ONOFF_CTRL0 = const(0x90)
_AXP2101_LDO_ONOFF_CTRL1 = const(0x91)
_AXP2101_LDO_VOL0_CTRL = const(0x92)
_AXP2101_LDO_VOL1_CTRL = const(0x93)
_AXP2101_LDO_VOL2_CTRL = const(0x94)
_AXP2101_LDO_VOL3_CTRL = const(0x95)
_AXP2101_LDO_VOL4_CTRL = const(0x96)
_AXP2101_LDO_VOL5_CTRL = const(0x97)
_AXP2101_LDO_VOL6_CTRL = const(0x98)
_AXP2101_LDO_VOL7_CTRL = const(0x99)
_AXP2101_LDO_VOL8_CTRL = const(0x9A)
_AXP2101_BAT_PARAME = const(0xA1)
_AXP2101_FUEL_GAUGE_CTRL = const(0xA2)
_AXP2101_BAT_PERCENT_DATA = const(0xA4)
# DCDC 1~5
_AXP2101_DCDC1_VOL_MIN = const(1500)
_AXP2101_DCDC1_VOL_MAX = const(3400)
_AXP2101_DCDC1_VOL_STEPS = const(100)
_AXP2101_DCDC2_VOL1_MIN = const(500)
_AXP2101_DCDC2_VOL1_MAX = const(1200)
_AXP2101_DCDC2_VOL2_MIN = const(1220)
_AXP2101_DCDC2_VOL2_MAX = const(1540)
_AXP2101_DCDC2_VOL_STEPS1 = const(10)
_AXP2101_DCDC2_VOL_STEPS2 = const(20)
_AXP2101_DCDC2_VOL_STEPS1_BASE = const(0)
_AXP2101_DCDC2_VOL_STEPS2_BASE = const(71)
_AXP2101_DCDC3_VOL1_MIN = const(500)
_AXP2101_DCDC3_VOL1_MAX = const(1200)
_AXP2101_DCDC3_VOL2_MIN = const(1220)
_AXP2101_DCDC3_VOL2_MAX = const(1540)
_AXP2101_DCDC3_VOL3_MIN = const(1600)
_AXP2101_DCDC3_VOL3_MAX = const(3400)
_AXP2101_DCDC3_VOL_MIN = const(500)
_AXP2101_DCDC3_VOL_MAX = const(3400)
_AXP2101_DCDC3_VOL_STEPS1 = const(10)
_AXP2101_DCDC3_VOL_STEPS2 = const(20)
_AXP2101_DCDC3_VOL_STEPS3 = const(100)
_AXP2101_DCDC3_VOL_STEPS1_BASE = const(0)
_AXP2101_DCDC3_VOL_STEPS2_BASE = const(71)
_AXP2101_DCDC3_VOL_STEPS3_BASE = const(88)
_AXP2101_DCDC4_VOL1_MIN = const(500)
_AXP2101_DCDC4_VOL1_MAX = const(1200)
_AXP2101_DCDC4_VOL2_MIN = const(1220)
_AXP2101_DCDC4_VOL2_MAX = const(1840)
_AXP2101_DCDC4_VOL_STEPS1 = const(10)
_AXP2101_DCDC4_VOL_STEPS2 = const(20)
_AXP2101_DCDC4_VOL_STEPS1_BASE = const(0)
_AXP2101_DCDC4_VOL_STEPS2_BASE = const(71)
_AXP2101_DCDC5_VOL_1200MV = const(1200)
_AXP2101_DCDC5_VOL_VAL = const(0x19)
_AXP2101_DCDC5_VOL_MIN = const(1400)
_AXP2101_DCDC5_VOL_MAX = const(3700)
_AXP2101_DCDC5_VOL_STEPS = const(100)
_AXP2101_VSYS_VOL_THRESHOLD_MIN = const(2600)
_AXP2101_VSYS_VOL_THRESHOLD_MAX = const(3300)
_AXP2101_VSYS_VOL_THRESHOLD_STEPS = const(100)
# ALDO 1~4
_AXP2101_ALDO1_VOL_MIN = const(500)
_AXP2101_ALDO1_VOL_MAX = const(3500)
_AXP2101_ALDO1_VOL_STEPS = const(100)
_AXP2101_ALDO2_VOL_MIN = const(500)
_AXP2101_ALDO2_VOL_MAX = const(3500)
_AXP2101_ALDO2_VOL_STEPS = const(100)
_AXP2101_ALDO3_VOL_MIN = const(500)
_AXP2101_ALDO3_VOL_MAX = const(3500)
_AXP2101_ALDO3_VOL_STEPS = const(100)
_AXP2101_ALDO4_VOL_MIN = const(500)
_AXP2101_ALDO4_VOL_MAX = const(3500)
_AXP2101_ALDO4_VOL_STEPS = const(100)
# BLDO 1~2
_AXP2101_BLDO1_VOL_MIN = const(500)
_AXP2101_BLDO1_VOL_MAX = const(3500)
_AXP2101_BLDO1_VOL_STEPS = const(100)
_AXP2101_BLDO2_VOL_MIN = const(500)
_AXP2101_BLDO2_VOL_MAX = const(3500)
_AXP2101_BLDO2_VOL_STEPS = const(100)
# CPUSLDO
_AXP2101_CPUSLDO_VOL_MIN = const(500)
_AXP2101_CPUSLDO_VOL_MAX = const(1400)
_AXP2101_CPUSLDO_VOL_STEPS = const(50)
# DLDO 1~2
_AXP2101_DLDO1_VOL_MIN = const(500)
_AXP2101_DLDO1_VOL_MAX = const(3400)
_AXP2101_DLDO1_VOL_STEPS = const(100)
_AXP2101_DLDO2_VOL_MIN = const(500)
_AXP2101_DLDO2_VOL_MAX = const(3400)
_AXP2101_DLDO2_VOL_STEPS = const(100)

AXP2101_SLAVE_ADDRESS = const(0x34)
XPOWERS_AXP2101_CHIP_ID = const(0x4A)


class AXP2101(I2CInterface):

    # ARGS ARGS ARGS ARGS ARGS ARGS ARGS ARGS ARGS

    """Power ON OFF IRQ timmint control values"""
    XPOWERS_AXP2101_IRQ_TIME_1S = const(0)
    XPOWERS_AXP2101_IRQ_TIME_1S5 = const(1)
    XPOWERS_AXP2101_IRQ_TIME_2S = const(2)
    XPOWERS_AXP2101_PRESSOFF_2S5 = const(3)

    """Precharge current limit values"""
    XPOWERS_AXP2101_PRECHARGE_25MA = const(1)
    XPOWERS_AXP2101_PRECHARGE_50MA = const(2)
    XPOWERS_AXP2101_PRECHARGE_75MA = const(3)
    XPOWERS_AXP2101_PRECHARGE_100MA = const(4)
    XPOWERS_AXP2101_PRECHARGE_125MA = const(5)
    XPOWERS_AXP2101_PRECHARGE_150MA = const(6)
    XPOWERS_AXP2101_PRECHARGE_175MA = const(7)
    XPOWERS_AXP2101_PRECHARGE_200MA = const(8)

    """Charging termination of current limit"""
    XPOWERS_AXP2101_CHG_ITERM_0MA = const(0)
    XPOWERS_AXP2101_CHG_ITERM_25MA = const(1)
    XPOWERS_AXP2101_CHG_ITERM_50MA = const(2)
    XPOWERS_AXP2101_CHG_ITERM_75MA = const(3)
    XPOWERS_AXP2101_CHG_ITERM_100MA = const(4)
    XPOWERS_AXP2101_CHG_ITERM_125MA = const(5)
    XPOWERS_AXP2101_CHG_ITERM_150MA = const(6)
    XPOWERS_AXP2101_CHG_ITERM_175MA = const(7)
    XPOWERS_AXP2101_CHG_ITERM_200MA = const(8)

    """Thermal regulation threshold setting"""
    XPOWERS_AXP2101_THREMAL_60DEG = const(0)
    XPOWERS_AXP2101_THREMAL_80DEG = const(1)
    XPOWERS_AXP2101_THREMAL_100DEG = const(2)
    XPOWERS_AXP2101_THREMAL_120DEG = const(3)

    """Charging  status values"""
    XPOWERS_AXP2101_CHG_TRI_STATE = const(0)  # tri_charge
    XPOWERS_AXP2101_CHG_PRE_STATE = const(1)  # pre_charge
    XPOWERS_AXP2101_CHG_CC_STATE = const(2)  # constant charge
    XPOWERS_AXP2101_CHG_CV_STATE = const(3)  # constant voltage
    XPOWERS_AXP2101_CHG_DONE_STATE = const(4)  # charge done
    XPOWERS_AXP2101_CHG_STOP_STATE = const(5)  # not chargin

    """PMU wakeup method values"""
    XPOWERS_AXP2101_WAKEUP_IRQ_PIN_TO_LOW = const(1 << 4)
    XPOWERS_AXP2101_WAKEUP_PWROK_TO_LOW = const(1 << 3)
    XPOWERS_AXP2101_WAKEUP_DC_DLO_SELECT = const(1 << 2)

    """Fast Power On start sequence values"""
    XPOWERS_AXP2101_FAST_DCDC1 = const(0)
    XPOWERS_AXP2101_FAST_DCDC2 = const(1)
    XPOWERS_AXP2101_FAST_DCDC3 = const(2)
    XPOWERS_AXP2101_FAST_DCDC4 = const(3)
    XPOWERS_AXP2101_FAST_DCDC5 = const(4)
    XPOWERS_AXP2101_FAST_ALDO1 = const(5)
    XPOWERS_AXP2101_FAST_ALDO2 = const(6)
    XPOWERS_AXP2101_FAST_ALDO3 = const(7)
    XPOWERS_AXP2101_FAST_ALDO4 = const(8)
    XPOWERS_AXP2101_FAST_BLDO1 = const(9)
    XPOWERS_AXP2101_FAST_BLDO2 = const(10)
    XPOWERS_AXP2101_FAST_CPUSLDO = const(11)
    XPOWERS_AXP2101_FAST_DLDO1 = const(12)
    XPOWERS_AXP2101_FAST_DLDO2 = const(13)

    """Fast Power On start sequence values"""
    XPOWERS_AXP2101_SEQUENCE_LEVEL_0 = const(0)
    XPOWERS_AXP2101_SEQUENCE_LEVEL_1 = const(1)
    XPOWERS_AXP2101_SEQUENCE_LEVEL_2 = const(2)
    XPOWERS_AXP2101_SEQUENCE_DISABLE = const(3)

    """Watchdog config values"""
    # Just interrupt to pin
    XPOWERS_AXP2101_WDT_IRQ_TO_PIN = const(0)
    # IRQ to pin and reset pmu system
    XPOWERS_AXP2101_WDT_IRQ_AND_RSET = const(1)
    # IRQ to pin and reset pmu systempull down pwrok
    XPOWERS_AXP2101_WDT_IRQ_AND_RSET_PD_PWROK = const(2)
    # IRQ to pin and reset pmu systemturn off dcdc & ldo pull down pwrok
    XPOWERS_AXP2101_WDT_IRQ_AND_RSET_ALL_OFF = const(3)

    """Watchdog timeout values"""
    XPOWERS_AXP2101_WDT_TIMEOUT_1S = const(0)
    XPOWERS_AXP2101_WDT_TIMEOUT_2S = const(1)
    XPOWERS_AXP2101_WDT_TIMEOUT_4S = const(2)
    XPOWERS_AXP2101_WDT_TIMEOUT_8S = const(3)
    XPOWERS_AXP2101_WDT_TIMEOUT_16S = const(4)
    XPOWERS_AXP2101_WDT_TIMEOUT_32S = const(5)
    XPOWERS_AXP2101_WDT_TIMEOUT_64S = const(6)
    XPOWERS_AXP2101_WDT_TIMEOUT_128S = const(7)

    """VBUS voltage limit values"""
    XPOWERS_AXP2101_VBUS_VOL_LIM_3V88 = const(0)
    XPOWERS_AXP2101_VBUS_VOL_LIM_3V96 = const(1)
    XPOWERS_AXP2101_VBUS_VOL_LIM_4V04 = const(2)
    XPOWERS_AXP2101_VBUS_VOL_LIM_4V12 = const(3)
    XPOWERS_AXP2101_VBUS_VOL_LIM_4V20 = const(4)
    XPOWERS_AXP2101_VBUS_VOL_LIM_4V28 = const(5)
    XPOWERS_AXP2101_VBUS_VOL_LIM_4V36 = const(6)
    XPOWERS_AXP2101_VBUS_VOL_LIM_4V44 = const(7)
    XPOWERS_AXP2101_VBUS_VOL_LIM_4V52 = const(8)
    XPOWERS_AXP2101_VBUS_VOL_LIM_4V60 = const(9)
    XPOWERS_AXP2101_VBUS_VOL_LIM_4V68 = const(10)
    XPOWERS_AXP2101_VBUS_VOL_LIM_4V76 = const(11)
    XPOWERS_AXP2101_VBUS_VOL_LIM_4V84 = const(12)
    XPOWERS_AXP2101_VBUS_VOL_LIM_4V92 = const(13)
    XPOWERS_AXP2101_VBUS_VOL_LIM_5V = const(14)
    XPOWERS_AXP2101_VBUS_VOL_LIM_5V08 = const(15)

    """VSYS power supply voltage limit values"""
    XPOWERS_AXP2101_VSYS_VOL_4V1 = const(0)
    XPOWERS_AXP2101_VSYS_VOL_4V2 = const(1)
    XPOWERS_AXP2101_VSYS_VOL_4V3 = const(2)
    XPOWERS_AXP2101_VSYS_VOL_4V4 = const(3)
    XPOWERS_AXP2101_VSYS_VOL_4V5 = const(4)
    XPOWERS_AXP2101_VSYS_VOL_4V6 = const(5)
    XPOWERS_AXP2101_VSYS_VOL_4V7 = const(6)
    XPOWERS_AXP2101_VSYS_VOL_4V8 = const(7)

    """Power on source values"""
    # POWERON low for on level when POWERON Mode as POWERON Source
    XPOWER_POWERON_SRC_POWERON_LOW = const(0)
    # IRQ PIN Pull-down as POWERON Source
    XPOWER_POWERON_SRC_IRQ_LOW = const(1)
    # Vbus Insert and Good as POWERON Source
    XPOWER_POWERON_SRC_VBUS_INSERT = const(2)
    # Vbus Insert and Good as POWERON Source
    XPOWER_POWERON_SRC_BAT_CHARGE = const(3)
    # Battery Insert and Good as POWERON Source
    XPOWER_POWERON_SRC_BAT_INSERT = const(4)
    # POWERON always high when EN Mode as POWERON Source
    XPOWER_POWERON_SRC_ENMODE = const(5)
    XPOWER_POWERON_SRC_UNKONW = const(6)  # Unkonw

    """Power off source values"""
    # POWERON Pull down for off level when POWERON Mode as POWEROFF Source
    XPOWER_POWEROFF_SRC_PWEKEY_PULLDOWN = const(0)
    # Software configuration as POWEROFF Source
    XPOWER_POWEROFF_SRC_SOFT_OFF = const(1)
    # POWERON always low when EN Mode as POWEROFF Source
    XPOWER_POWEROFF_SRC_PWEKEY_LOW = const(2)
    # Vsys Under Voltage as POWEROFF Source
    XPOWER_POWEROFF_SRC_UNDER_VSYS = const(3)
    # VBUS Over Voltage as POWEROFF Source
    XPOWER_POWEROFF_SRC_OVER_VBUS = const(4)
    # DCDC Under Voltage as POWEROFF Source
    XPOWER_POWEROFF_SRC_UNDER_VOL = const(5)
    # DCDC Over Voltage as POWEROFF Source
    XPOWER_POWEROFF_SRC_OVER_VOL = const(6)
    # Die Over Temperature as POWEROFF Source
    XPOWER_POWEROFF_SRC_OVER_TEMP = const(7)
    XPOWER_POWEROFF_SRC_UNKONW = const(8)  # Unkonw

    """Power ok signal delay values"""
    XPOWER_PWROK_DELAY_8MS = const(0)
    XPOWER_PWROK_DELAY_16MS = const(1)
    XPOWER_PWROK_DELAY_32MS = const(2)
    XPOWER_PWROK_DELAY_64MS = const(3)

    """Power button press shutdown time values"""
    XPOWERS_POWEROFF_4S = const(0)
    XPOWERS_POWEROFF_6S = const(1)
    XPOWERS_POWEROFF_8S = const(2)
    XPOWERS_POWEROFF_10S = const(3)

    """Power on time value when the power button is pressed"""
    XPOWERS_POWERON_128MS = const(0)
    XPOWERS_POWERON_512MS = const(1)
    XPOWERS_POWERON_1S = const(2)
    XPOWERS_POWERON_2S = const(3)

    """PMU LED indicator function values"""
    XPOWERS_CHG_LED_OFF = const(0)
    XPOWERS_CHG_LED_BLINK_1HZ = const(1)
    XPOWERS_CHG_LED_BLINK_4HZ = const(2)
    XPOWERS_CHG_LED_ON = const(3)
    XPOWERS_CHG_LED_CTRL_CHG = const(4)

    """Charging voltage limit values"""
    XPOWERS_AXP2101_CHG_VOL_4V = const(1)
    XPOWERS_AXP2101_CHG_VOL_4V1 = const(2)
    XPOWERS_AXP2101_CHG_VOL_4V2 = const(3)
    XPOWERS_AXP2101_CHG_VOL_4V35 = const(4)
    XPOWERS_AXP2101_CHG_VOL_4V4 = const(5)

    _CHG_VOL = (
        XPOWERS_AXP2101_CHG_VOL_4V,
        XPOWERS_AXP2101_CHG_VOL_4V1,
        XPOWERS_AXP2101_CHG_VOL_4V2,
        XPOWERS_AXP2101_CHG_VOL_4V35,
        XPOWERS_AXP2101_CHG_VOL_4V4
    )

    """Charging current limit values"""
    XPOWERS_AXP2101_CHG_CUR_100MA = const(4)
    XPOWERS_AXP2101_CHG_CUR_125MA = const(5)
    XPOWERS_AXP2101_CHG_CUR_150MA = const(6)
    XPOWERS_AXP2101_CHG_CUR_175MA = const(7)
    XPOWERS_AXP2101_CHG_CUR_200MA = const(8)
    XPOWERS_AXP2101_CHG_CUR_300MA = const(9)
    XPOWERS_AXP2101_CHG_CUR_400MA = const(10)
    XPOWERS_AXP2101_CHG_CUR_500MA = const(11)
    XPOWERS_AXP2101_CHG_CUR_600MA = const(12)
    XPOWERS_AXP2101_CHG_CUR_700MA = const(13)
    XPOWERS_AXP2101_CHG_CUR_800MA = const(14)
    XPOWERS_AXP2101_CHG_CUR_900MA = const(15)
    XPOWERS_AXP2101_CHG_CUR_1000MA = const(16)

    _CHG_CUR = (
        XPOWERS_AXP2101_CHG_CUR_100MA,
        XPOWERS_AXP2101_CHG_CUR_125MA,
        XPOWERS_AXP2101_CHG_CUR_150MA,
        XPOWERS_AXP2101_CHG_CUR_175MA,
        XPOWERS_AXP2101_CHG_CUR_200MA,
        XPOWERS_AXP2101_CHG_CUR_300MA,
        XPOWERS_AXP2101_CHG_CUR_400MA,
        XPOWERS_AXP2101_CHG_CUR_500MA,
        XPOWERS_AXP2101_CHG_CUR_600MA,
        XPOWERS_AXP2101_CHG_CUR_700MA,
        XPOWERS_AXP2101_CHG_CUR_800MA,
        XPOWERS_AXP2101_CHG_CUR_900MA,
        XPOWERS_AXP2101_CHG_CUR_1000MA,
    )

    """VBUS current limit values"""
    XPOWERS_AXP2101_VBUS_CUR_LIM_100MA = const(0)
    XPOWERS_AXP2101_VBUS_CUR_LIM_500MA = const(1)
    XPOWERS_AXP2101_VBUS_CUR_LIM_900MA = const(2)
    XPOWERS_AXP2101_VBUS_CUR_LIM_1000MA = const(3)
    XPOWERS_AXP2101_VBUS_CUR_LIM_1500MA = const(4)
    XPOWERS_AXP2101_VBUS_CUR_LIM_2000MA = const(5)

    _VBUS_LIMIT = (
        XPOWERS_AXP2101_VBUS_CUR_LIM_100MA,
        XPOWERS_AXP2101_VBUS_CUR_LIM_500MA,
        XPOWERS_AXP2101_VBUS_CUR_LIM_900MA,
        XPOWERS_AXP2101_VBUS_CUR_LIM_1000MA,
        XPOWERS_AXP2101_VBUS_CUR_LIM_1500MA,
        XPOWERS_AXP2101_VBUS_CUR_LIM_2000MA,
    )

    """PMU interrupt control mask values"""

    #! IRQ1 REG 40H
    XPOWERS_AXP2101_BAT_NOR_UNDER_TEMP_IRQ = const(
        1 << 0)   # Battery Under Temperature in Work
    XPOWERS_AXP2101_BAT_NOR_OVER_TEMP_IRQ = const(
        1 << 1)   # Battery Over Temperature in Work mode
    # Battery Under Temperature in Charge mode IRQ(bcut_irq)
    XPOWERS_AXP2101_BAT_CHG_UNDER_TEMP_IRQ = const(1 << 2)
    # Battery Over Temperature in Charge mode IRQ(bcot_irq) enable
    XPOWERS_AXP2101_BAT_CHG_OVER_TEMP_IRQ = const(1 << 3)
    # Gauge New SOC IRQ(lowsoc_irq) enable ???
    XPOWERS_AXP2101_GAUGE_NEW_SOC_IRQ = const(1 << 4)
    # Gauge Watchdog Timeout IRQ(gwdt_irq) enable
    XPOWERS_AXP2101_WDT_TIMEOUT_IRQ = const(1 << 5)
    # SOC drop to Warning Level1 IRQ(socwl1_irq) enable
    XPOWERS_AXP2101_WARNING_LEVEL1_IRQ = const(1 << 6)
    # SOC drop to Warning Level2 IRQ(socwl2_irq) enable
    XPOWERS_AXP2101_WARNING_LEVEL2_IRQ = const(1 << 7)

    #! IRQ2 REG 41H
    # POWERON Positive Edge IRQ(ponpe_irq_en) enable
    XPOWERS_AXP2101_PKEY_POSITIVE_IRQ = const(1 << 8)
    # POWERON Negative Edge IRQ(ponne_irq_en) enable
    XPOWERS_AXP2101_PKEY_NEGATIVE_IRQ = const(1 << 9)
    # POWERON Long PRESS IRQ(ponlp_irq) enable
    XPOWERS_AXP2101_PKEY_LONG_IRQ = const(1 << 10)
    # POWERON Short PRESS IRQ(ponsp_irq_en) enable
    XPOWERS_AXP2101_PKEY_SHORT_IRQ = const(1 << 11)
    # Battery Remove IRQ(bremove_irq) enable
    XPOWERS_AXP2101_BAT_REMOVE_IRQ = const(1 << 12)
    # Battery Insert IRQ(binsert_irq) enabl
    XPOWERS_AXP2101_BAT_INSERT_IRQ = const(1 << 13)
    XPOWERS_AXP2101_VBUS_REMOVE_IRQ = const(
        1 << 14)  # VBUS Remove IRQ(vremove_irq) enabl
    # VBUS Insert IRQ(vinsert_irq) enable
    XPOWERS_AXP2101_VBUS_INSERT_IRQ = const(1 << 15)

    #! IRQ3 REG 42H
    # Battery Over Voltage Protection IRQ(bovp_irq) enable
    XPOWERS_AXP2101_BAT_OVER_VOL_IRQ = const(1 << 16)
    # Charger Safety Timer1/2 expire IRQ(chgte_irq) enable
    XPOWERS_AXP2101_CHAGER_TIMER_IRQ = const(1 << 17)
    # DIE Over Temperature level1 IRQ(dotl1_irq) enable
    XPOWERS_AXP2101_DIE_OVER_TEMP_IRQ = const(1 << 18)
    XPOWERS_AXP2101_BAT_CHG_START_IRQ = const(
        1 << 19)  # Charger start IRQ(chgst_irq) enable
    # Battery charge done IRQ(chgdn_irq) enable
    XPOWERS_AXP2101_BAT_CHG_DONE_IRQ = const(1 << 20)
    # BATFET Over Current Protection IRQ(bocp_irq) enable
    XPOWERS_AXP2101_BATFET_OVER_CURR_IRQ = const(1 << 21)
    # LDO Over Current IRQ(ldooc_irq) enable
    XPOWERS_AXP2101_LDO_OVER_CURR_IRQ = const(1 << 22)
    # Watchdog Expire IRQ(wdexp_irq) enable
    XPOWERS_AXP2101_WDT_EXPIRE_IRQ = const(1 << 23)
    XPOWERS_AXP2101_ALL_IRQ = const(0xFFFFFFFF)

    def __init__(self, i2c_bus: I2C, addr: int = AXP2101_SLAVE_ADDRESS) -> None:
        super().__init__(i2c_bus, addr)
        print('AXP2101 __init__')
        self.statusRegister = [0] * _AXP2101_INTSTS_CNT
        self.intRegister = [0] * _AXP2101_INTSTS_CNT

        if self.getChipID() != XPOWERS_AXP2101_CHIP_ID:
            raise RuntimeError(
                "Failed to find %s - check your wiring!" % self.__class__.__name__
            )

    # getBatPresentState
    def isBatteryConnect(self) -> bool:
        return bool(super().getRegisterBit(_AXP2101_STATUS1, 3))

    def isBatInActiveModeState(self) -> bool:
        return bool(super().getRegisterBit(_AXP2101_STATUS1, 2))

    def enableFastWakeup(self) -> None:
        super().setRegisterBit(_AXP2101_FAST_PWRON_CTRL, 6)

    def disableFastWakeup(self) -> None:
        super().clrRegisterBit(_AXP2101_FAST_PWRON_CTRL, 6)

    def disableGeneralAdcChannel(self) -> None:
        super().clrRegisterBit(_AXP2101_ADC_CHANNEL_CTRL, 5)

    def enableTemperatureMeasure(self) -> None:
        super().setRegisterBit(_AXP2101_ADC_CHANNEL_CTRL, 4)

    def disableTemperatureMeasure(self) -> None:
        super().clrRegisterBit(_AXP2101_ADC_CHANNEL_CTRL, 4)

    def getTemperature(self) -> float:
        raw = super().readRegisterH6L8(_AXP2101_ADC_DATA_RELUST8, _AXP2101_ADC_DATA_RELUST9)
        return (22.0 + (7274 - raw) / 20.0)

    def enableSystemVoltageMeasure(self) -> None:
        super().setRegisterBit(_AXP2101_ADC_CHANNEL_CTRL, 3)

    def disableSystemVoltageMeasure(self) -> None:
        super().clrRegisterBit(_AXP2101_ADC_CHANNEL_CTRL, 3)

    def getSystemVoltage(self) -> int:
        return super().readRegisterH6L8(_AXP2101_ADC_DATA_RELUST6, _AXP2101_ADC_DATA_RELUST7)

    def enableVbusVoltageMeasure(self) -> None:
        super().setRegisterBit(_AXP2101_ADC_CHANNEL_CTRL, 2)

    def disableVbusVoltageMeasure(self) -> None:
        super().clrRegisterBit(_AXP2101_ADC_CHANNEL_CTRL, 2)

    def getVbusVoltage(self) -> int:
        return super().readRegisterH6L8(_AXP2101_ADC_DATA_RELUST4, _AXP2101_ADC_DATA_RELUST5)

    def enableTSPinMeasure(self) -> None:
        super().setRegisterBit(_AXP2101_ADC_CHANNEL_CTRL, 1)

    def disableTSPinMeasure(self) -> None:
        super().clrRegisterBit(_AXP2101_ADC_CHANNEL_CTRL, 1)

    def enableTSPinLowFreqSample(self) -> None:
        super().setRegisterBit(_AXP2101_ADC_CHANNEL_CTRL, 7)

    def disableTSPinLowFreqSample(self) -> None:
        super().clrRegisterBit(_AXP2101_ADC_DATA_RELUST2, 7)

    def getTsTemperature(self) -> int:
        return super().readRegisterH6L8(_AXP2101_ADC_DATA_RELUST2, _AXP2101_ADC_DATA_RELUST3)

    def enableBattVoltageMeasure(self) -> None:
        super().setRegisterBit(_AXP2101_ADC_CHANNEL_CTRL, 0)

    def disableBattVoltageMeasure(self) -> None:
        super().clrRegisterBit(_AXP2101_ADC_CHANNEL_CTRL, 0)

    def enableBattDetection(self) -> None:
        super().setRegisterBit(_AXP2101_BAT_DET_CTRL, 0)

    def disableBattDetection(self) -> None:
        super().clrRegisterBit(_AXP2101_BAT_DET_CTRL, 0)

    def getBattVoltage(self) -> int:
        if not self.isBatteryConnect():
            return 0
        return super().readRegisterH5L8(_AXP2101_ADC_DATA_RELUST0, _AXP2101_ADC_DATA_RELUST1)

    def getBatteryPercent(self) -> int:
        if not self.isBatteryConnect():
            return -1
        return super().readRegister(_AXP2101_BAT_PERCENT_DATA)[0]

    # CHG LED setting and control
    # @brief Set charging led mode.
    def setChargingLedMode(self, mode: int) -> None:
        range = [self.XPOWERS_CHG_LED_OFF, self.XPOWERS_CHG_LED_BLINK_1HZ,
                 self.XPOWERS_CHG_LED_BLINK_4HZ, self.XPOWERS_CHG_LED_ON]
        if mode in range:
            val = super().readRegister(_AXP2101_CHGLED_SET_CTRL)[0]
            val &= 0xC8
            val |= 0x05  # use manual ctrl
            val |= (mode << 4)
            super().writeRegister(_AXP2101_CHGLED_SET_CTRL, val)
        else:
            val = super().readRegister(_AXP2101_CHGLED_SET_CTRL)[0]
            val &= 0xF9
            super().writeRegister(_AXP2101_CHGLED_SET_CTRL, val | 0x01)  # use type A mode

    def getChargingLedMode(self) -> int:
        val = super().readRegister(_AXP2101_CHGLED_SET_CTRL)[0]
        val >>= 1
        if (val & 0x02) == 0x02:
            val >>= 4
            return val & 0x03
        return self.XPOWERS_CHG_LED_CTRL_CHG

    # @brief 预充电充电电流限制
    # @note  Precharge current limit 25N mA
    # @param   opt: 25  opt
    # # @retval None
    def setPrechargeCurr(self, opt: int) -> None:
        val = super().readRegister(_AXP2101_IPRECHG_SET)[0]
        val &= 0xFC
        super().writeRegister(_AXP2101_IPRECHG_SET, val | opt)

    def getPrechargeCurr(self) -> None:
        return (super().readRegister(_AXP2101_IPRECHG_SET)[0] & 0x03)

     # @brief Set charge current.
     # @param   opt: See _axp2101_chg_curr_t enum for details.
     # @retval
    def setChargerConstantCurr(self, opt: int) -> None:
        if not 4 <= opt <= 16:
            raise ValueError(
                "Charger Constant Current must be a value within 4-16!")
        val = super().readRegister(_AXP2101_ICC_CHG_SET)[0]
        val &= 0xE0
        super().writeRegister(_AXP2101_ICC_CHG_SET, val | opt)

    # @brief Get charge current settings.
    # @retval See _axp2101_chg_curr_t enum for details.

    def getChargerConstantCurr(self) -> int:
        return (super().readRegister(_AXP2101_ICC_CHG_SET)[0] & 0x1F)

    # @brief  充电终止电流限制
    # @note   Charging termination of current limit

    def setChargerTerminationCurr(self, opt: int) -> None:
        val = super().readRegister(_AXP2101_ITERM_CHG_SET_CTRL)[0]
        val &= 0xF0
        super().writeRegister(_AXP2101_ICC_CHG_SET, val | opt)

    def getChargerTerminationCurr(self) -> int:
        return (super().readRegister(_AXP2101_ITERM_CHG_SET_CTRL)[0] & 0x0F)

    def enableChargerTerminationLimit(self) -> None:
        val = super().readRegister(_AXP2101_ITERM_CHG_SET_CTRL)[0]
        super().writeRegister(_AXP2101_ITERM_CHG_SET_CTRL, val | 0x10)

    def disableChargerTerminationLimit(self) -> None:
        val = super().readRegister(_AXP2101_ITERM_CHG_SET_CTRL)[0]
        super().writeRegister(_AXP2101_ITERM_CHG_SET_CTRL, val & 0xEF)

    def isChargerTerminationLimit(self) -> bool:
        return bool(super().getRegisterBit(_AXP2101_ITERM_CHG_SET_CTRL, 4))

    # @brief Set charge target voltage.
    # @param   opt: See _axp2101_chg_vol_t enum for details.

    def setChargeTargetVoltage(self, opt: int) -> None:
        if not 1 <= opt <= 5:
            raise ValueError(
                "Charger target voltage must be a value within 0-3!")
        val = super().readRegister(_AXP2101_CV_CHG_VOL_SET)[0]
        val &= 0xFC
        super().writeRegister(_AXP2101_CV_CHG_VOL_SET, val | opt)

    # @brief Get charge target voltage settings.
    # @retval See _axp2101_chg_vol_t enum for details.

    def getChargeTargetVoltage(self) -> int:
        return (super().readRegister(_AXP2101_CV_CHG_VOL_SET)[0] & 0x03)

    # @brief  设定热阈值
    # @note   Thermal regulation threshold setting
    def setThermaThreshold(self, opt: int) -> None:
        val = super().readRegister(_AXP2101_THE_REGU_THRES_SET)[0]
        val &= 0xFC
        super().writeRegister(_AXP2101_THE_REGU_THRES_SET, val | opt)

    def getThermaThreshold(self) -> int:
        return (super().readRegister(_AXP2101_THE_REGU_THRES_SET)[0] & 0x03)

    def getBatteryParameter(self) -> int:
        return super().readRegister(_AXP2101_BAT_PARAME)[0]

    def fuelGaugeControl(self, writeROM: bool, enable: bool) -> int:
        if writeROM:
            super().clrRegisterBit(_AXP2101_FUEL_GAUGE_CTRL, 4)
        else:
            super().setRegisterBit(_AXP2101_FUEL_GAUGE_CTRL, 4)

        if enable:
            super().setRegisterBit(_AXP2101_FUEL_GAUGE_CTRL, 0)
        else:
            super().clrRegisterBit(_AXP2101_FUEL_GAUGE_CTRL, 0)

    #  Interrupt status/control functions
    # @brief  Get the interrupt controller mask value.
    # @retval   Mask value corresponds to _axp2101_irq_t ,

    def getIrqStatus(self) -> int:
        self.statusRegister = super().readRegister(_AXP2101_INTSTS1, 3)
        return (self.statusRegister[0] << 16) | (self.statusRegister[1] << 8) | (self.statusRegister[2])

    def isBatChargerOverTemperatureIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_BAT_CHG_OVER_TEMP_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isBatChargerUnderTemperatureIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_BAT_CHG_UNDER_TEMP_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isBatWorkOverTemperatureIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_BAT_NOR_OVER_TEMP_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    def isBatWorkUnderTemperatureIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_BAT_NOR_UNDER_TEMP_IRQ
        if self.intRegister[0] & mask:
            return super()._IS_BIT_SET(self.statusRegister[0], mask)
        else:
            return False

    # IRQ STATUS 1
    def isVbusInsertIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_VBUS_INSERT_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isVbusRemoveIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_VBUS_REMOVE_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isBatInsertIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_BAT_INSERT_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    def isBatRemoveIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_BAT_REMOVE_IRQ >> 8
        if self.intRegister[1] & mask:
            return super()._IS_BIT_SET(self.statusRegister[1], mask)
        else:
            return False

    # IRQ STATUS 2
    def isWdtExpireIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_WDT_EXPIRE_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isLdoOverCurrentIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_LDO_OVER_CURR_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isBatfetOverCurrentIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_BATFET_OVER_CURR_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isBatChagerDoneIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_BAT_CHG_DONE_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isBatChagerStartIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_BAT_CHG_START_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isBatDieOverTemperatureIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_DIE_OVER_TEMP_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isChagerOverTimeoutIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_CHAGER_TIMER_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def isBatOverVoltageIrq(self) -> bool:
        mask = self.XPOWERS_AXP2101_BAT_OVER_VOL_IRQ >> 16
        if self.intRegister[2] & mask:
            return super()._IS_BIT_SET(self.statusRegister[2], mask)
        else:
            return False

    def getChipID(self) -> int:
        return super().readRegister(_AXP2101_IC_TYPE)[0]
