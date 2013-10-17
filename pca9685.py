import smbus
import math
import time

import RPi.GPIO as GPIO

class PCA9685(object):
    __SUBADR1            = 0x02
    __SUBADR2            = 0x03
    __SUBADR3            = 0x04
    __MODE1              = 0x00
    __PRESCALE           = 0xFE
    __LED0_ON_L          = 0x06
    __LED0_ON_H          = 0x07
    __LED0_OFF_L         = 0x08
    __LED0_OFF_H         = 0x09
    __ALLLED_ON_L        = 0xFA
    __ALLLED_ON_H        = 0xFB
    __ALLLED_OFF_L       = 0xFC
    __ALLLED_OFF_H       = 0xFD

    def __init__(self, address, oe = None):
        self._oe = oe

        self._address = address
        self._bus = smbus.SMBus(1)
        self._bus.write_byte_data(self._address, self.__MODE1, 0x00)

    def enable(self, value):
        if self._oe is not None:
            GPIO.output(self._oe, not value)

    def set(self, channel, on, off):
        on = int(max(0, min(0xfff, on)))
        off = int(max(0, min(0xfff, off)))

        self._bus.write_byte_data(self._address, self.__LED0_ON_L + 4*channel, on & 0xFF)
        self._bus.write_byte_data(self._address, self.__LED0_ON_H + 4*channel, on >> 8)
        self._bus.write_byte_data(self._address, self.__LED0_OFF_L + 4*channel, off & 0xFF)
        self._bus.write_byte_data(self._address, self.__LED0_OFF_H + 4*channel, off >> 8)

    def frequency(self, f):
        prescaleval = 25000000.0    # 25MHz
        prescaleval /= 4096.0       # 12-bit
        prescaleval /= float(f)
        prescale = math.floor(prescaleval - 0.5)

        oldmode = self._bus.read_byte_data(self._address, self.__MODE1)
        newmode = (oldmode & 0x7F) | 0x10

        self._bus.write_byte_data(self._address, self.__MODE1, newmode)
        self._bus.write_byte_data(self._address, self.__PRESCALE, int(math.floor(prescale)))
        self._bus.write_byte_data(self._address, self.__MODE1, oldmode)

        time.sleep(0.005)
        self._bus.write_byte_data(self._address, self.__MODE1, oldmode | 0x80)
