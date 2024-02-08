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
move1 = 1       # move to position 1
home = 0        # home value to travel to
t_hang = 1.5    # wait time between successive gotoDogleg calls

# set reset command - just run shell script
stopXMS = './killXCD2.sh'
startXMS = './startXMS.sh'
reset = './debug_reset_doglegs.sh'

# Initialize file to store movement report
REPORTFILE = ''
PORTFILE = 'XCD_current_port'

# Iterate over all serial controllers we find matching /dev/ttyUSB*
ttyUSB_ports = find_ttyUSB_ports()
# ttyUSB_ports = ['/dev/ttyUSB0']



def resetDogleg():
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

def testBoards():

    for ser in ttyUSB_ports:
        # check if port exists
        if os.path.exists(ser):
            with open(PORTFILE, 'r') as file:
                file.write(ser)
            print(">>>>>>>testing controller on", ser, "...")

            # check status, then initialize proper variables
            status=readback(ADDR['STATUS'])
            if status!=0:
                print("exerciseDogleg.py initilization failed. Please check status.")
                return
            
            writeXCD2(['XAXIS', 0])
            writeXCD2(['VEL', 100])
            writeXCD2(['FPOS', 0])
            writeXCD2([ADDR['TURNS'], 0])
            writeXCD2(['XAXIS', 1])
            writeXCD2(['VEL', 100])
            writeXCD2(['FPOS', 0])
            writeXCD2([ADDR['TURNS'], 0])

            # start on XAXIS 0
            print(">>>>>>>AXIS 0:")
            writeXCD2(['XAXIS', 0])
            time.sleep(t_hang)
        
            # move first to high bound and if timeout then reset
            succ1, posi1 = gotoDogleg(move1)
            time.sleep(t_hang)

             # move first to high bound and if timeout then reset
            succ2, posi2 = gotoDogleg(home)
            time.sleep(t_hang)

            # switch to XAXIS 1
            print(">>>>>>>AXIS 1:")
            writeXCD2(['XAXIS', 1])
            time.sleep(t_hang)

            # move first to high bound and if timeout then reset
            succ3, posi3 = gotoDogleg(move1)
            time.sleep(t_hang)

             # move first to high bound and if timeout then reset
            succ4, posi4 = gotoDogleg(home)
            time.sleep(t_hang)

        else:
            print("port not found by shell.  Huh?")
    return


if __name__ == "__main__":
    #check args
    if len(sys.argv) == 1:
        testBoards()
    else:
        sys.exit()