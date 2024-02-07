#! /usr/bin/python3

import os
import sys
import time
from xcdSerial import getCurrentPort
from updatePorts import find_ttyUSB_ports
from quickAssign import writeXCD2
from quickReport import readback
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from gotoDogleg import gotoDogleg

# SET GLOBAL VARIABLES
lb = -2.9       # low bound to travel to
home = 0        # home value to travel to
hb = 2.9        # high bound to travel to
t_hang = 1.5    # wait time between successive gotoDogleg calls

# set reset command - just run shell script
stopXMS = './killXCD2.sh'
startXMS = './startXMS.sh'
reset = './debug_reset_doglegs.sh'

# Initialize file to store movement report
REPORTFILE = ''

# Iterate over all serial controllers we find matching /dev/ttyUSB*
# ttyUSB_ports = find_ttyUSB_ports()
# ttyUSB_ports = ['/dev/ttyUSB0']


def resetAttenuator():
    currentAx = readback(ADDR['XAXIS'])
    os.system(stopXMS)
    os.system(startXMS)
    writeXCD2([ADDR['STATUS'], 0])
    writeXCD2(['XAXIS', 0])
    writeXCD2(['VEL', 100])
    writeXCD2(['XAXIS', 1])
    writeXCD2(['VEL', 100])
    writeXCD2(['XAXIS', currentAx])
    return


def exerciseAttenuator( loop=True ):

    # pulls current port from PORTFILE (specified in xcdSerial)
    ttyUSB_port = getCurrentPort()

    # check if port exists
    if os.path.exists(ttyUSB_port):
        print(">>>>>>>testing controller on", ttyUSB_port, "...")

        # strip directory and name REPORTFILE as which USB - different ports will
        # generate different files
        whichUSB = ttyUSB_port.lstrip('/dev/tty')
        REPORTFILE = whichUSB + '_doglegReport.txt'

        # guarantees back and forth will run at least once
        init_run = True

        return
    
if __name__ == "__main__":
    #check args
    if len(sys.argv) == 1:
        exerciseAttenuator()
    elif len(sys.argv) == 2:
        if sys.argv[1] == 0:
            exerciseAttenuator(loop=False)
        else
            print("second argument can only be 0 to denote False for loop condition.")
            sys.exit()
    else:
    else:
        sys.exit()