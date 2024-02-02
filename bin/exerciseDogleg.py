#! /usr/bin/python3

import os
import sys
import time
from xcdSerial import getCurrentPort
from updatePorts import find_ttyUSB_ports
from quickAssign import writeXCD2
from quickReport import readback, reportXCD2
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from gotoDogleg import gotoDogleg

# SET GLOBAL VARIABLES
lb = -2.9       # low bound to travel to
home = 0        # home value to travel to
hb = 2.9        # high bound to travel to
t_hang = 1.5    # wait time between successive gotoDogleg calls

# set reset command - just run shell script
reset = './debug_reset_doglegs.sh'

# Initialize file to store movement report
REPORTFILE = ''

# Iterate over all serial controllers we find matching /dev/ttyUSB*
# ttyUSB_ports = find_ttyUSB_ports()
# ttyUSB_ports = ['/dev/ttyUSB0']



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

        # initialize proper variables
        suc01, ret01 = reportXCD2([ADDR['STATUS']])
        writeXCD2(['XAXIS', 0])
        writeXCD2(['VEL', 100])
        writeXCD2(['FPOS', 0])
        writeXCD2([ADDR['TURNS'], 0])
        suc02, ret02 = reportXCD2([ADDR['STATUS']])

        suc11, ret11 = reportXCD2([ADDR['STATUS']])
        writeXCD2(['XAXIS', 1])
        writeXCD2(['VEL', 100])
        writeXCD2(['FPOS', 0])
        writeXCD2([ADDR['TURNS'], 0])
        suc12, ret12 = reportXCD2([ADDR['STATUS']])

        # if status is not waiting, say initialization failed
        if (not suc01) or (not suc02) or (not suc11) or (not suc12):
            print("exerciseDogleg.py initilization failed. Please check status.")
            return

        # for each run, cycle through axes
        while init_run:

            t_arr = [0.0]*12
            posi = [0.0]*6

            tRunStart = time.time()

            print(">>>>>>>AXIS 0:")
            writeXCD2(['XAXIS', 0])
        
            # t_arr[0] = time.time()
            # succ, posi[0] = gotoDogleg(hb)
            # t_arr[1] = time.time()
            # time.sleep(t_hang)

            # t_arr[2] = time.time()
            # succ, posi[1] = gotoDogleg(lb)
            # t_arr[3] = time.time()
            # time.sleep(t_hang)

            # t_arr[4] = time.time()
            # succ, posi[2] = gotoDogleg(home)
            # t_arr[5] = time.time()
            # time.sleep(t_hang)

        
            print(">>>>>>>AXIS 1:")
            writeXCD2(['XAXIS', 1])
        
            time.sleep(t_hang)

            t_arr[6] = time.time()
            succ, posi[3] =  gotoDogleg(hb)
            if not succ:
                os.system(reset)
                return
            t_arr[7] = time.time()
            time.sleep(t_hang)

            t_arr[8] = time.time()
            succ, posi[4] = gotoDogleg(lb)
            t_arr[9] = time.time()
            time.sleep(t_hang)

            t_arr[10] = time.time()
            succ, posi[5] = gotoDogleg(home)
            t_arr[11] = time.time()


            print("exerciseDogleg.py REPORT:",
                "\n AXIS 0: readWrite time = ", t_arr[1]-t_arr[0],
                "\n\t home{:.4g}-->hb{:.4g}: ".format(home, posi[0]), t_arr[2]-t_arr[1], 
                "\n\t hb{:.4g}-->lb{:.4g}: ".format(posi[0], posi[1]), t_arr[3]-t_arr[2], 
                "\n\t lb{:.4g}-->home{:.4g}: ".format(posi[1], posi[2]), t_arr[4]-t_arr[3],
                "\n AXIS 1: readWrite time = ", t_arr[6]-t_arr[5],
                "\n\t home{:.4g}-->hb{:.4g}: ".format(home, posi[3]), t_arr[7]-t_arr[6], 
                "\n\t hb{:.4g}-->lb{:.4g}: ".format(posi[3], posi[4]), t_arr[8]-t_arr[7],
                "\n\t lb{:.4g}-->home{:.4g}: ".format(posi[4], posi[5]), t_arr[9]-t_arr[8])
            
            with open(REPORTFILE, "a") as file:
                file.write('%s %s %s %s %s %s %s\n' % (tRunStart, t_arr[2]-t_arr[1], t_arr[3]-t_arr[2],
                                                    t_arr[4]-t_arr[3], t_arr[7]-t_arr[6], 
                                                    t_arr[8]-t_arr[7], t_arr[9]-t_arr[8]))
                
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

