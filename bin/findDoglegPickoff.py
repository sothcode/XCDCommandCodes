#! /usr/bin/python3

import os
import sys
import time
from xcdSerial import getCurrentPort
from updatePorts import find_ttyUSB_ports
from quickAssign import writeXCD2
from quickReport import readback
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT 
from changeAxisDogleg import changeAxis
from gotoDogleg import gotoDogleg
from clearDogleg import clearDogleg

# SET GLOBAL VARIABLES
lb = -2.9                       # low bound to travel to
hb = 2.9                        # high bound to travel to
ss = 0.1                        # step size to take in search
numsteps = int((hb-lb)/ss - 1)  # numsteps to take

# set reset command - just run shell script
stopXMS = './killXCD2.sh'
startXMS = './startXMS.sh'


def _reverseLookup(dict,val):
    #set up the reverse dictionary
    reverse_mapping={v: k for k, v in dict.items()}
    try:
        key=reverse_mapping[val]
    except KeyError as e:
        print(f"errorCode lookup failed.  KeyError: {e}")
        sys.exit()
    return key  


def gridSearch( input_dogleg ):

    # label axes to move from input dogleg
    DL_A0 = input_dogleg + '_A0'
    DL_A1 = input_dogleg + '_A1'

    # start by moving chosen dogleg to (-2.9, 2.9)
    init_A0 = changeAxis(DL_A0)
    goto_A0, pos0 = gotoDogleg(lb)
    init_A1 = changeAxis(DL_A1)
    goto_A1, pos1 = gotoDogleg(lb)
    if not (init_A0 and goto_A0 and init_A1 and goto_A1):
        return

    # define initial moves
    move_A0 = hb
    move_A1 = lb + ss

    for i in range(numsteps):

        # change to DL0
        didChangeAxis = changeAxis(DL_A0)

        # move A0 from to either lb or hb
        didGoto, pos = gotoDogleg(move_A0)

        # change to DL1
        didChangeAxis = changeAxis(DL_A1)

        # move A1 up by step size ss
        didGoto, pos = gotoDogleg(move_A1)

        x = input("Press enter to perform next move.  Press any key then enter to abort.")
        if x != "":
            return
        else:
            move_A0 = -1*move_A0
            move_A1 = move_A1 + ss

    print("findDoglegPickoff:gridSearch finished.")

    return




def spiralSearch():



    return



if __name__ == "__main__":
    #check args
    if len(sys.argv) == 2:
        input_dl = sys.argv[1]
        gridSearch( input_dl )
    else:
        print("")
        sys.exit()
