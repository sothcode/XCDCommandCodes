#! /usr/bin/python3

from talkNano import main

import sys

def homeNano (argv):
    if argv:
        command_send = []
        command_code = "b1:4"
        command_send.append(command_code)

        method_val = str(argv[0])

        if method_val in {"50","51","60","61"}:
            method_code = "i2:" + method_val
            command_send.append(method_code)
        else:
            print("Value to assign - " + method_val + " - must be 50, 51, 60, or 61.")
            return

        for item in range(1,len(argv)):
            var_num = str(argv[item])
            try:
                float(var_num)
            except ValueError:
                print("Value to assign - " + var_num + " - must be a real number.")
                return
            var_code = "r4:" + var_num
            command_send.append(var_code)

        if len(command_send) > 5:
            print( "4 Maximum arguments allowed.")
            return
        else:
            print(command_send)
            main(command_send)
            return
    else:
        print(" \
 No arguments given. homeNano parameters are: \n \
 1) Method- Mandatory, determines the method of homing. \n \
    50 = home on negative hard-stop. \n \
    51 = home on positive hard-stop. \n \
    60 = Home on negative hard-stop and index pulse \n \
    61 = home on positive hard stop and index pulse. \n \
 2) Origin - Optional, Defines position of home point. Real value, [mm]  \n \
 3) Velocity 1 - Optional, Defines the first stage velocity. Real value, [mm/2] \n \
 4) Velocity 2 - Optional, Defines the second stage velocity. Real value, [mm/2] \n \
 ")

        return

if __name__ == "__main__":
    homeNano(sys.argv[1:])
