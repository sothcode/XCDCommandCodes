#!/usr/bin/python3

import sys
import os
from quickReport import readback
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varUniqueID as AXID


def whichLaser():
    currentID = readback(ADDR['ID'])
    IDlookup = {v:k for k, v in AXID.items()}
    print(IDlookup[currentID])


if __name__ == "__main__":
    debug=True
    whichLaser()
