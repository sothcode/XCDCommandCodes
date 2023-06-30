#! /usr/bin/python3

from talkNano import main
from variableDictionary import varDict


import sys

def reportNano (argv):
    if argv:
        command_send = []
        command_code = "b1:26"
        command_send.append(command_code)
        for item in argv:
            var_name = str(item)
            if var_name in varDict.keys():
                var_num = str(varDict[var_name])
                var_code = "u2:" + var_num
                command_send.append(var_code)
            else:
                print("Variable name "+ var_name + " not recognized. Please refer to variable list.")
                return
        if len(command_send) > 11:
            print ( "Maximum number of variables to report at a time is 10. Please request fewer variables.")
            return
        else:
            print(command_send)
            msg = main(command_send)
            return msg
    else:
        print(" \
 No arguments given. reportNano parameters are: \n \
 1) Variable- Mandatory, variable to report value of. For full list of variables, refer to variableDictionary. \n \
 2-10) Variable - Optional, other variables to report. \
 ")
        return


if __name__ == "__main__":
    reportNano(sys.argv[1:])
