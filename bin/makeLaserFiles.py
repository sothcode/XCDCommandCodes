#! /usr/bin/python3
import sys
import os
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varUniqueID as AXID

debug = False

for axisName in AXID:

    filename = axisName
    with open(os.path.join('/mnt/c/Users/smh28/Documents/Github/XCDCommandCodes/laserFiles', filename), "w") as file:

        for varName, varVal in ADDR.items():
            enr = 6.103515625e-5
            axis = 0
            if (AXID[axisName] % 2) == 0:
                axis = 1
            
            if varVal == 'ID':
                file.write('ID %s\n' % AXID[axisName])
            elif varVal == 'XAXIS':
                file.write('ID %s\n' % axis)
            elif varVal == 'ENR':
                file.write('ID %s\n' % enr)
            else:
                file.write('%s %s\n' % (varVal, 0.0))