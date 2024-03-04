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
from clearDogleg import clearDogleg

# SET GLOBAL VARIABLES
lb = -2.9       # low bound to travel to
home = 0        # home value to travel to
hb = 2.9        # high bound to travel to
t_hang = 0.5    # wait time between successive gotoDogleg calls

# set reset command - just run shell script
stopXMS = './killXCD2.sh'
startXMS = './startXMS.sh'



def findDoglegPickoff():

    # pulls current port from PORTFILE (specified in xcdSerial)
    ttyUSB_port = getCurrentPort()

    # check if port exists
    if os.path.exists(ttyUSB_port):
        print(">>>>>>>testing controller on", ttyUSB_port, "...")

        # check status, then initialize proper variables
        status=readback(ADDR['STATUS'])
        if status!=0:
            print("findDoglegPickoff.py initilization failed. Please check status.")
            return

        t_arr = [0.0]*12
        stat = [0.0]*6
        posi = [0.0]*6

        tRunStart = time.time()

        # start on XAXIS 0
        print(">>>>>>>AXIS 0:")
        writeXCD2(['XAXIS', 0])
        time.sleep(t_hang)
    
        # move first to high bound and if timeout then reset
        t_arr[0] = time.time()
        succ, posi[0] = gotoDogleg(hb)
        t_arr[1] = time.time()
        if not succ:
            stat[0] = readback(ADDR['STATUS'])
            clearDogleg()
        time.sleep(t_hang)

    else:
        print("port not found by shell.  Huh?")

    return


if __name__ == "__main__":
    #check args
    if len(sys.argv) == 1:
        findDoglegPickoff()
    else:
        sys.exit()
