#! /usr/bin/python3

from talkNano import main

import sys

def configNano (argv) :

    command_send = []
    command_code = "b1:80"
    command_send.append(command_code)

    if argv:
        level_val = str(argv[0])
        try:
            float(level_val)
        except ValueError:
            print( "PWM value - " + level_val + " - needs to be a real number")
            return
        level_code = "r4:" + level_val
        command_send.append(level_code)

        width_val = str(argv[1])
        try:
            float(width_val)
        except ValueError:
            print( "PWM width - " + width_val + " - needs to be a real number")
            return
        width_code = "r4:" + width_val
        command_send.append(width_code)

        thresh_val = str(argv[2])
        try:
            float(thresh_val)
        except ValueError:
            print( "Threshold value - " + thresh_val + " - needs to be a real number")
            return
        thresh_code = "r4:" + thresh_val
        command_send.append(thresh_code)


    else:
        print("No arguments given. Default calibration values applied.")

    if len(command_send) > 4:
        print("3 maximum arguments allowed")
        return
    else:
#        print(command_send)
        main(command_send)
        return

if __name__ == "__main__":
    configNano(sys.argv[1:])
