#! /usr/bin/python3

############################## IMPORTANT ##############################
# This program builds off of reportNano.py by interpreting the feedback 
# from the TPC Pi to see if there are any errors being thrown.
#######################################################################

from commNano import main
from variableDictionary import varDict

import sys


def statusNano (argv = "Status"):

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
            print("Variable name "+ var_name + 
            " not recognized. Please refer to variable list.")
            return
    if len(command_send) > 11:
        print ( "Maximum number of variables to report at a time is 10. Please request fewer variables.")
        return
    else:
        e = main(command_send)
    
    # main(command_send) will return a string of the form b'\x1a\x01\x00\x14\x05\x02'

    



if __name__ == "__main__":
    statusNano(sys.argv[1:])