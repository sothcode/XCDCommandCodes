#! /usr/bin/python3

from talkNano import main
from variableDictionary import varDict

import sys

def assignNano ( argv ):
    if argv:
        command_send = []
        command_code = "b1:3"
        command_send.append(command_code)

        var_name = str(argv[0])
        if var_name in varDict.keys():
            var_num = str(varDict[var_name])
            var_code = "u2:" + var_num
            command_send.append(var_code)
        else:
            print("Variable name - " + var_name + " -  not recognized. Variable list given as:")
            print(varDict.keys())
            return

        real_value = str(argv[1])
        try:
            float(real_value)
        except ValueError:
            print("Value to assign - " + real_value + " - must be a real number.")
            return
        real_code = "r4:" + real_value
        command_send.append(real_code)
        print(command_send)
        main(command_send)
        return
    else:
        print(" \
 No arguments given. assignNano parameters are: \n \
 1) Variable- Mandatory, determines the variable to change the value of. Refer to variableDictionary for a full list of variables. \n \
 2) Value - Mandatory, determines value to change variable to. Real value.  \n \
 ")
        return

if __name__ == "__main__":
    assignNano(sys.argv[1:])

