#! /usr/bin/python3
from talkNano import main

import sys

def moveNano ( pos_value ):
    if pos_value:
        command_send = []
        command_code = "b1:1"
        command_send.append(command_code)

        
        pos_code = "r4:" + str(pos_value)
        command_send.append(pos_code)

        print(command_send)
        main(command_send)
        return
    else:
        print(" \
 No arguments given. moveNano parameters are: \n \
 1) Position- Mandatory, Defines taget position to move to. Real value, [mm] \
 ")
        return


if __name__ == "__main__":
    pos_value = str(sys.argv[1])
    try:
        float(pos_value)
    except ValueError:
        print("Position to move to - " + pos_value + " - must be a real number in mm.")
        sys.exit()
    moveNano(pos_value)
