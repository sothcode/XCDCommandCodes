#! /usr/bin/python3

import os
import sys
import time
from quickReport import readback
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
        didChange_A0 = changeAxis(DL_A0)
        if not didChange_A0:
            print("findDoglegPickoff change to A0 failed on step ", i)
            return

        # move A0 from to either lb or hb
        didGoto_A0, pos0 = gotoDogleg(move_A0)
        if not didGoto_A0:
            if pos0 == 0:
                print("findDoglegPickoff A0 move step ", i, " to ", pos0, " failed.")
                return
            else:
                x = input("gotoDogleg failed with above status. Press enter to clear or any other key then enter to abort.")
                if x != "":
                    return
                else:
                    clearDogleg()


        # change to DL1
        didChange_A1 = changeAxis(DL_A1)
        if not didChange_A1:
            print("findDoglegPickoff change to A1 failed on step ", i)
            return

        # move A1 up by step size ss
        didGoto_A1, pos1 = gotoDogleg(move_A1)
        if not didGoto_A1:
            if pos1 == 0:
                print("findDoglegPickoff A1 move step ", i, " to ", pos1, " failed.")
                return
            else:
                x = input("gotoDogleg failed with above status. Press enter to clear or any other key then enter to abort.")
                if x != "":
                    return
                else:
                    clearDogleg()


        x = input("Press enter to perform next move.  Press any key then enter to abort.")
        if x != "":
            return
        else:
            move_A0 = -1*move_A0
            move_A1 = move_A1 + ss

    print("findDoglegPickoff:gridSearch finished.")

    return




def spiralSearch( input_dogleg ):

    # label axes to move from input dogleg
    DL_A0 = input_dogleg + '_A0'
    DL_A1 = input_dogleg + '_A1'

    move_size = ss

    # for i in range():

    # start by moving chosen dogleg to (-2.9, 2.9)
    init_A0 = changeAxis(DL_A0)

    return



if __name__ == "__main__":
    #check args
    if len(sys.argv) == 2:
        input_dl = sys.argv[1]
        gridSearch( input_dl )
    else:
        print("")
        sys.exit()
