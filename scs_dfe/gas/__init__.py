"""
Created on 16 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_dfe.gas.ads1115 import ADS1115
from scs_dfe.gas.mcp3425 import MCP3425
from scs_dfe.gas.sensor import Sensor
from scs_dfe.gas.temp_comp import TempComp


# --------------------------------------------------------------------------------------------------------------------

ADS1115.init()

MCP3425.init()

Sensor.init()

TempComp.init()
