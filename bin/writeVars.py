#!/usr/bin/python3

import sys
import os
from quickAssign import writeXCD2
from quickReport import readback, reportXCD2
from xcdSerial import getCurrentPort
from variableDictionaryXCD2 import varDict
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from variableDictionaryXCD2 import varDoglegCommands as COMM
from variableDictionaryXCD2 import varUniqueID as AXID

# to load tty data from the db so we know which tty we want:
sys.path.append("kfDatabase")
import kfDatabase


# tuning settings
sleeptime=0.5 #in seconds
debug=False
portsDb="xcd2_ports.kfdb"
PORTFILE="XCD_current_port"



def writeToFile( filename ):

    with open(filename + '.txt', "w") as file:
        # go thru varDict
        for varName in varDict:

            # report every variable from varDict
            check, varVal = reportXCD2([varName])

            if check==False:
                print("CRITICAL FAILURE. Communication error.")
                sys.exit()
        
            if debug:
                print("_readback result: ", varVal[0])
        
            # Logs the change to the log for a change
            file.write('%s %s\n' % (varName, varVal[0]))
            print('Controller values written to ' + filename + '.txt')


    return 

if __name__ == "__main__":
    # check args
    # if wrong arguments, exit with explanation
    if len(sys.argv) == 2: # sys.argv has arg 1 as the command itself
        writeToFile(sys.argv[1])
    else:
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is:")
        print("   ./writeVars.py \"filename\"")
        sys.exit()