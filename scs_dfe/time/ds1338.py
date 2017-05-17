"""
Created on 16 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Note: time should always be stored as UTC, then localized on retrieval.
"""

import sys

from scs_core.data.rtc_datetime import RTCDatetime

from scs_host.bus.i2c import I2C


# --------------------------------------------------------------------------------------------------------------------

class DS1338(object):
    """
    Maxim Integrated DS1338 serial real-time clock
    """
    __ADDR =                0x68

    __REG_SECONDS =         0x00
    __REG_MINUTES =         0x01
    __REG_HOURS =           0x02
    __REG_DAY =             0x03
    __REG_DATE =            0x04
    __REG_MONTH =           0x05
    __REG_YEAR =            0x06
    __REG_CONTROL =         0x07

    __RAM_START_ADDR =      0x08

    __MASK_CLOCK_HALT =     0x80        # ---- 1000 0000

    __MASK_SQW_EN =         0x10        # ---- 0001 0000
    __MASK_OSC_STOPPED =    0x20        # ---- 0010 0000


    # ----------------------------------------------------------------------------------------------------------------
    # clock...

    @classmethod
    def init(cls):
        # TODO: set 24 Hr, no SQWE
        pass


    @classmethod
    def get_time(cls):
        # read RTC...
        second = cls.__read_reg_decimal(cls.__REG_SECONDS)
        minute = cls.__read_reg_decimal(cls.__REG_MINUTES)
        hour = cls.__read_reg_decimal(cls.__REG_HOURS)

        weekday = cls.__read_reg_decimal(cls.__REG_DAY)

        day = cls.__read_reg_decimal(cls.__REG_DATE)
        month = cls.__read_reg_decimal(cls.__REG_MONTH)
        year = cls.__read_reg_decimal(cls.__REG_YEAR)

        rtc_datetime = RTCDatetime(year, month, day, weekday, hour, minute, second)

        return rtc_datetime


    @classmethod
    def set_time(cls, rtc_datetime):
        # update RTC...
        cls.__write_reg_decimal(cls.__REG_SECONDS, rtc_datetime.second)
        cls.__write_reg_decimal(cls.__REG_MINUTES, rtc_datetime.minute)
        cls.__write_reg_decimal(cls.__REG_HOURS, rtc_datetime.hour)

        cls.__write_reg_decimal(cls.__REG_DAY, rtc_datetime.weekday)

        cls.__write_reg_decimal(cls.__REG_DATE, rtc_datetime.day)
        cls.__write_reg_decimal(cls.__REG_MONTH, rtc_datetime.month)
        cls.__write_reg_decimal(cls.__REG_YEAR, rtc_datetime.year)


    @classmethod
    def square_wave(cls, enabled):
        value = cls.__read_reg(cls.__REG_CONTROL)
        value = value | cls.__MASK_SQW_EN if enabled else value & ~cls.__MASK_SQW_EN

        cls.__write_reg(cls.__REG_CONTROL, value)


    @classmethod
    def dump(cls):
        # read RTC...
        second = cls.__read_reg(cls.__REG_SECONDS)
        minute = cls.__read_reg(cls.__REG_MINUTES)
        hour = cls.__read_reg(cls.__REG_HOURS)

        weekday = cls.__read_reg(cls.__REG_DAY)

        day = cls.__read_reg(cls.__REG_DATE)
        month = cls.__read_reg(cls.__REG_MONTH)
        year = cls.__read_reg(cls.__REG_YEAR)

        control = cls.__read_reg(cls.__REG_CONTROL)

        # print...
        print("seconds: 0x%02x" % second, file=sys.stderr)
        print("minutes: 0x%02x" % minute, file=sys.stderr)
        print("  hours: 0x%02x" % hour, file=sys.stderr)

        print("weekday: 0x%02x" % weekday, file=sys.stderr)

        print("    day: 0x%02x" % day, file=sys.stderr)
        print("  month: 0x%02x" % month, file=sys.stderr)
        print("   year: 0x%02x" % year, file=sys.stderr)

        print("control: 0x%02x" % control, file=sys.stderr)

        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # RAM...

    @classmethod
    def read(cls, addr):
        return cls.__read_reg(cls.__RAM_START_ADDR + addr)


    @classmethod
    def write(cls, addr, val):
        cls.__write_reg(cls.__RAM_START_ADDR + addr, val)


    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __read_reg_decimal(cls, addr):
        return cls.__as_decimal(cls.__read_reg(addr))


    @classmethod
    def __read_reg(cls, addr):
        try:
            I2C.start_tx(cls.__ADDR)
            value = I2C.read_cmd(addr, 1)
        finally:
            I2C.end_tx()

        return value


    @classmethod
    def __write_reg_decimal(cls, addr, value):
        return cls.__write_reg(addr, cls.__as_bcd(value))


    @classmethod
    def __write_reg(cls, addr, value):
        try:
            I2C.start_tx(cls.__ADDR)
            I2C.write(addr, value)
        finally:
            I2C.end_tx()


    @classmethod
    def __as_decimal(cls, bcd):
        msb = bcd >> 4
        lsb = bcd & 0x0f

        return msb * 10 + lsb


    @classmethod
    def __as_bcd(cls, decimal):
        msb = decimal // 10
        lsb = decimal % 10

        return msb << 4 | lsb
