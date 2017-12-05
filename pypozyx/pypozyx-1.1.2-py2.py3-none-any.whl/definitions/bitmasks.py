#!/usr/bin/env python
"""pypozyx.definitions.bitmasks - contains all bitmasks used in Pozyx functionality, such as interrupt flags."""

# Bit mask for POZYX_ST_RESULT
POZYX_ST_RESULT_ACC = 0x01
POZYX_ST_RESULT_MAGN = 0x02
POZYX_ST_RESULT_GYR = 0x04
POZYX_ST_RESULT_MCU = 0x08
POZYX_ST_RESULT_PRES = 0x10
POZYX_ST_RESULT_UWB = 0x20

# Bit mask for POZYX_INT_STATUS
POZYX_INT_STATUS_ERR = 0x01
POZYX_INT_STATUS_POS = 0x02
POZYX_INT_STATUS_IMU = 0x04
POZYX_INT_STATUS_RX_DATA = 0x08
POZYX_INT_STATUS_FUNC = 0x10

# Bit mask for POZYX_INT_MASK
POZYX_INT_MASK_ERR = 0x01
POZYX_INT_MASK_POS = 0x02
POZYX_INT_MASK_IMU = 0x04
POZYX_INT_MASK_RX_DATA = 0x08
POZYX_INT_MASK_FUNC = 0x10
POZYX_INT_MASK_TDMA = 0x40
POZYX_INT_MASK_PIN = 0x80
POZYX_INT_MASK_ALL = 0x1F

# Bit mask for POZYX_LED_CTRL
POZYX_LED_CTRL_LED1 = 0x01
POZYX_LED_CTRL_LED2 = 0x02
POZYX_LED_CTRL_LED3 = 0x04
POZYX_LED_CTRL_LED4 = 0x08

# Bit mask for device type
POZYX_TYPE = 0xE0
