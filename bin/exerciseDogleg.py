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


def exerciseDogleg( loop=True ):

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

        # for each run, cycle through axes
        while init_run:

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
                resetDogleg()
            time.sleep(t_hang)

            # then move to low bound and if timeout then reset
            t_arr[2] = time.time()
            succ, posi[1] = gotoDogleg(lb)
            t_arr[3] = time.time()
            if not succ:
                stat[1] = readback(ADDR['STATUS'])
                resetDogleg()
            time.sleep(t_hang)

            # last move home and if timeout then reset
            t_arr[4] = time.time()
            succ, posi[2] = gotoDogleg(home)
            t_arr[5] = time.time()
            time.sleep(t_hang)
            if not succ:
                stat[2] = readback(ADDR['STATUS'])
                resetDogleg()
            time.sleep(t_hang)

            # switch to XAXIS 1
            print(">>>>>>>AXIS 1:")
            writeXCD2(['XAXIS', 1])
            time.sleep(t_hang)

            # and repeat moving to hb, lb then home with XAXIS 1 (with resets)
            t_arr[6] = time.time()
            succ, posi[3] = gotoDogleg(hb)
            t_arr[7] = time.time()
            if not succ:
                stat[3] = readback(ADDR['STATUS'])
                resetDogleg()
            time.sleep(t_hang)


            t_arr[8] = time.time()
            succ, posi[4] = gotoDogleg(lb)
            t_arr[9] = time.time()
            if not succ:
                stat[4] = readback(ADDR['STATUS'])
                resetDogleg()
            time.sleep(t_hang)


            t_arr[10] = time.time()
            succ, posi[5] = gotoDogleg(home)
            t_arr[11] = time.time()
            if not succ:
                stat[5] = readback(ADDR['STATUS'])
                resetDogleg()


            print("exerciseDogleg.py REPORT: startTime = ", tRunStart,
                "\n AXIS 0:", "\n\t home ({:.5g}) --> hb ({:.5g}): ".format(home, posi[0]), t_arr[1]-t_arr[0], 
                "\n\t hb ({:.5g}) --> lb ({:.5g}): ".format(posi[0], posi[1]), t_arr[3]-t_arr[2], 
                "\n\t lb ({:.5g}) --> home ({:.5g}): ".format(posi[1], posi[2]), t_arr[5]-t_arr[4],
                "\n AXIS 1:", "\n\t home ({:.5g}) --> hb ({:.4g}): ".format(home, posi[3]), t_arr[7]-t_arr[6], 
                "\n\t (hb{:.5g}) --> lb ({:.5g}): ".format(posi[3], posi[4]), t_arr[9]-t_arr[8],
                "\n\t (lb{:.5g}) --> home ({:.5g}): ".format(posi[4], posi[5]), t_arr[11]-t_arr[10])
            
            with open(REPORTFILE, "a") as file:
                file.write('%s %s %s %s %s %s %s %s %s %s %s %s %s\n' 
                           % (tRunStart, t_arr[1]-t_arr[0], stat[0], t_arr[3]-t_arr[2], stat[1],
                            t_arr[5]-t_arr[4], stat[2], t_arr[7]-t_arr[6], stat[3],
                            t_arr[9]-t_arr[8], stat[4], t_arr[11]-t_arr[10], stat[5]))
                
            init_run = loop

    else:
        print("port not found by shell.  Huh?")

    return

if __name__ == "__main__":
    #check args
    if len(sys.argv) == 1:
        exerciseDogleg()
    elif len(sys.argv) == 2:
        if sys.argv[1] == False:
            exerciseDogleg(loop=False)
        sys.exit()
    else:
        sys.exit()

