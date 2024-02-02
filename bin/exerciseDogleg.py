#! /usr/bin/python3

import os
import time
from updatePorts import find_ttyUSB_ports
from quickAssign import writeXCD2
from quickReport import reportXCD2
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from gotoDogleg import gotoDogleg

lb = -2.9
home = 0
hb = 2.9
PORTFILE = "XCD_current_port"
REPORTFILE = "exerciseDoglegReport.txt"


# Iterate over all serial controllers we find matching /dev/ttyUSB*
ttyUSB_ports = find_ttyUSB_ports()
ttyUSB_ports = ['/dev/ttyUSB0']

iter = 1

while True:
    for ser in ttyUSB_ports:
        # check if the file exists
        if os.path.exists(ser):
            print(">>>>>>>testing controller on", ser, "...")
            with open(PORTFILE, "w") as file:
                file.write(ser)
            print(">>>>>>>AXIS 0:")

            t_arr = [0.0]*10
            succ = [None]*6
            posi = [0.0]*6

            # t_arr[0] = time.time()

            # suc01, ret01 = reportXCD2([ADDR['STATUS'], 'XAXIS'])
            # writeXCD2([ADDR['XAXIS'], 0])
            # writeXCD2([ADDR['FPOS'], 0])
            # writeXCD2([ADDR['TURNS'], 0])
            # suc02, ret02 = reportXCD2([ADDR['STATUS'], 'XAXIS'])
        
            # t_arr[1] = time.time()
            # succ[0], posi[0] = gotoDogleg(hb)
            # t_arr[2] = time.time()
            # succ[1], posi[1] = gotoDogleg(lb)
            # t_arr[3] = time.time()
            # succ[2], posi[2] = gotoDogleg(home)
            # t_arr[4] = time.time()

        
            print(">>>>>>>AXIS 1:")

            t_arr[5] = time.time()

            suc11, ret11 = reportXCD2([ADDR['STATUS'], 'XAXIS'])
            writeXCD2([ADDR['XAXIS'], 1])
            writeXCD2([ADDR['FPOS'], 0])
            writeXCD2([ADDR['TURNS'], 0])
            suc12, ret12 = reportXCD2([ADDR['STATUS'], 'XAXIS'])
        
            t_arr[6] = time.time()
            succ[3], posi[3] =  gotoDogleg(hb)
            t_arr[7] = time.time()
            succ[4], posi[4] = gotoDogleg(lb)
            t_arr[8] = time.time()
            succ[5], posi[5] = gotoDogleg(home)
            t_arr[9] = time.time()

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
                file.write('%s %s %s\n' % ("Iteration ", iter, ": \n"))
                file.write('%s %s %s %s %s %s\n' % (t_arr[2]-t_arr[1], t_arr[3]-t_arr[2],
                                                    t_arr[4]-t_arr[3], t_arr[7]-t_arr[6], 
                                                    t_arr[8]-t_arr[7], t_arr[9]-t_arr[8]))

        else:
            print("port not found by shell.  Huh?")

    iter += 1
