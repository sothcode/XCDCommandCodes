#! /usr/bin/python3

import time
from xcdSerial import sendline
from variableDictionaryXCD2 import varDict
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
import sys
import struct

debug=False

def saveToFlash():

    return