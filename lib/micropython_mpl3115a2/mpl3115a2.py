# SPDX-FileCopyrightText: Copyright (c) 2023 Jose D. Montoya
#
# SPDX-License-Identifier: MIT
"""
`mpl3115a2`
================================================================================

MicroPython driver for the NXP MPL3115A2 Pressure and Temperature sensor


* Author(s): Jose D. Montoya


"""

import time
import struct
from micropython import const
from micropython_mpl3115a2.i2c_helpers import CBits, RegisterStruct


__version__ = "0.1.0"
__repo__ = "https://github.com/jposada202020/MicroPython_MPL3115A2.git"

_REG_WHOAMI = const(0x0C)

_MPL3115A2_ADDRESS = const(0x60)
_REGISTER_STATUS = const(0x00)
_DATA = const(0x01)
_BAR_IN_MSB = const(0x14)
_BAR_IN_LSB = const(0x15)
_PT_DATA_CFG = const(0x13)
_CTRL_REG1 = const(0x26)
_CTRL_REG2 = const(0x27)


OS1 = const(0b000)
OS2 = const(0b001)
OS4 = const(0b010)
OS8 = const(0b011)
OS16 = const(0b100)
OS32 = const(0b101)
OS64 = const(0b110)
OS128 = const(0b111)
oversample_ratio_values = (OS1, OS2, OS4, OS8, OS16, OS32, OS64, OS128)


class MPL3115A2:
    """Driver for the MPL3115A2 Sensor connected over I2C.

    :param ~machine.I2C i2c: The I2C bus the MPL3115A2 is connected to.
    :param int address: The I2C device address. Defaults to :const:`0x60`

    :raises RuntimeError: if the sensor is not found

    **Quickstart: Importing and using the device**

    Here is an example of using the :class:`MPL3115A2` class.
    First you will need to import the libraries to use the sensor

    .. code-block:: python

        from machine import Pin, I2C
        from micropython_mpl3115a2 import mpl3115a2

    Once this is done you can define your `machine.I2C` object and define your sensor object

    .. code-block:: python

        i2c = I2C(1, sda=Pin(2), scl=Pin(3))
        mpl3115a2 = mpl3115a2.MPL3115A2(i2c)

    Now you have access to the attributes

    .. code-block:: python

    """

    _device_id = RegisterStruct(_REG_WHOAMI, "B")

    _device_control = RegisterStruct(_CTRL_REG1, "B")
    _data_config = RegisterStruct(_PT_DATA_CFG, "B")
    _register_status = RegisterStruct(_REGISTER_STATUS, "B")
    _sea_level_pressure_msb = RegisterStruct(_BAR_IN_MSB, "B")
    _sea_level_pressure_lsb = RegisterStruct(_BAR_IN_LSB, "B")

    _alt_enabled = CBits(1, _CTRL_REG1, 7)
    _oversample_ratio = CBits(3, _CTRL_REG1, 3)
    _reset_status = CBits(1, _CTRL_REG1, 2)
    _ost_status = CBits(1, _CTRL_REG1, 1)

    _pdr_status = CBits(1, _REGISTER_STATUS, 2)
    _tmp_status = CBits(1, _REGISTER_STATUS, 1)

    def __init__(self, i2c, address: int = 0x60) -> None:
        self._i2c = i2c
        self._address = address

        if self._device_id != 0xC4:
            raise RuntimeError("Failed to find MPL3115A2")

        self._data_config = 0b111

    @property
    def oversample_ratio(self) -> str:
        """
        Sensor oversample_ratio

        +-----------------------------+-------------------+
        | Mode                        | Value             |
        +=============================+===================+
        | :py:const:`mpl3115a2.OS1`   | :py:const:`0b000` |
        +-----------------------------+-------------------+
        | :py:const:`mpl3115a2.OS2`   | :py:const:`0b001` |
        +-----------------------------+-------------------+
        | :py:const:`mpl3115a2.OS4`   | :py:const:`0b010` |
        +-----------------------------+-------------------+
        | :py:const:`mpl3115a2.OS8`   | :py:const:`0b011` |
        +-----------------------------+-------------------+
        | :py:const:`mpl3115a2.OS16`  | :py:const:`0b100` |
        +-----------------------------+-------------------+
        | :py:const:`mpl3115a2.OS32`  | :py:const:`0b101` |
        +-----------------------------+-------------------+
        | :py:const:`mpl3115a2.OS64`  | :py:const:`0b110` |
        +-----------------------------+-------------------+
        | :py:const:`mpl3115a2.OS128` | :py:const:`0b111` |
        +-----------------------------+-------------------+
        """
        values = ("OS1", "OS2", "OS4", "OS8", "OS16", "OS32", "OS64", "OS128")
        return values[self._oversample_ratio]

    @oversample_ratio.setter
    def oversample_ratio(self, value: int) -> None:
        if value not in oversample_ratio_values:
            raise ValueError("Value must be a valid oversample_ratio setting")
        self._oversample_ratio = value

    @property
    def pressure(self) -> float:
        """
        Read the barometric pressure detected by the sensor in Hectopascals.
        """

        data = bytearray(5)
        self._poll_reg1()
        self._alt_enabled = 0
        self._ost_status = 1  # Set OST to 1 to start measurement.

        while self._pdr_status == 0:
            time.sleep(0.01)

        self._i2c.readfrom_mem_into(self._address, _DATA, data)

        pressure = ((data[0] << 16) | (data[1] << 8) | data[2]) & 0xFFFFFF
        pressure >>= 4

        return pressure / 400.0

    def _poll_reg1(self) -> None:
        """
        Poll the ost_status to NOT be present.
        """
        while self._ost_status > 0:
            time.sleep(0.01)

    @property
    def altitude(self) -> float:
        """Read the altitude as calculated based on the sensor pressure and
        previously configured pressure at sea-level.  This will return a
        value in meters.  Set the sea-level pressure by updating the
        :attr:`sealevel_pressure` property first to get a more accurate altitude value.
        """
        data = bytearray(5)
        self._poll_reg1()
        self._alt_enabled = 1
        self._ost_status = 1
        while self._pdr_status == 0:
            time.sleep(0.01)
        self._i2c.readfrom_mem_into(self._address, _DATA, data)

        data[3] = 0
        altitude = struct.unpack(">i", data[0:4])[0]

        return altitude / 65535.0

    @property
    def temperature(self) -> float:
        """
        Read the temperature as measured by the sensor in Celsius.
        """
        data = bytearray(5)
        self._poll_reg1()
        self._ost_status = 1

        while self._tmp_status == 0:
            time.sleep(0.01)

        self._i2c.readfrom_mem_into(self._address, _DATA, data)

        temperature = struct.unpack(">h", data[3:5])[0]
        temperature >>= 4

        return temperature / 16.0

    @property
    def sealevel_pressure(self) -> float:
        """
        Read and write the pressure at sea-level used to calculate altitude.
        """
        pressure = (self._sea_level_pressure_msb << 8) | self._sea_level_pressure_lsb

        return pressure * 2.0 / 100

    @sealevel_pressure.setter
    def sealevel_pressure(self, val: float) -> None:
        bars = int(val * 50)
        self._sea_level_pressure_lsb = bars & 0xFF
        self._sea_level_pressure_msb = bars >> 8
