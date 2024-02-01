#! /usr/bin/python3

from talkNano import main

import sys

def pulseNano (argv) :
    if argv:
        command_send = []
        command_code = "b1:33"
        command_send.append(command_code)

        start_val = str(argv[0])
        try:
            float(start_val)
        except ValueError:
            print( "Starting value - " + start_val + " - needs to be a real number")
            return
        start_code = "r4:" + start_val
        command_send.append(start_code)

        incr_val = str(argv[1])
        try:
            float(incr_val)
        except ValueError:
            print( "Increment value - " + incr_val + " - needs to be a real number")
            return
        incr_code = "r4:" + incr_val
        command_send.append(incr_code)

        count_val = str(argv[2])
        try:
            int(count_val)
        except ValueError:
            print( "Count value - " + count_val + " - needs to be an integer")
            return
        count_code = "i4:" + count_val
        command_send.append(count_code)

        if len(command_send) > 4:
            print("3 maximum arguments allowed")
            return
        else:
            print(command_send)
            main(command_send)
            return
    else:
        print(" \
 No arguments given. pulseNano parameters are: \n \
 1) Start - Mandatory, specifies the first position. Real value. \n \
 2) Increment - Mandatory, specifies the distance between pulses. Real value, [mm]  \n \
 3) Count - Mandatory, specifies the number of pulses. Integer.  \n \
 ")


        return

if __name__ == "__main__":
    pulseNano(sys.argv[1:])
