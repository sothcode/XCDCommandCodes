#!/usr/bin/python3

import sys
import os
from quickAssign import writeXCD2
from quickReport import readback, reportXCD2
from variableDictionaryXCD2 import varDict
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from variableDictionaryXCD2 import varDoglegCommands as COMM
from variableDictionaryXCD2 import varUniqueID as AXID
#import random #for testing

#tuning settings
sleeptime=0.5 #in seconds
debug=False


def writeToFile( filename ):

    with open(filename, "w") as file:
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


    return 


def readFromFile( filename ):

    if not os.path.isfile(filename):
        print("Couldn't read from file. Variables not updated.")
        return False

    with open(filename, "r") as file:
        for line in file:
            (varName, varVal) = line.split()

            writeXCD2([varName, varVal])
        
    return True


def changeAxis( targetIDstr ):

    #check if controller is busy.  If so, exit with explanation
    if debug:
        print("changeAxis:  Check status:")
    status=readback(ADDR['STATUS'])

    if status!=0:
        if status == 98.0:
            print("Axis must be set by calling setAxis.py")

        else:
            print("NOT EXECUTED. Controller status is not 0.")
            sys.exit()

    if targetIDstr not in AXID.keys():
        print("Axis ID - " + targetIDstr + " -  not recognized. Axis ID list given as:")
        print(AXID.keys())
        sys.exit()
    
    currentID = readback(ADDR['ID'])

    targetID = AXID[targetIDstr]

    if currentID == targetID:
        print("Target axis is same as current axis.")
        return

    # create lookup table of axis variables
    IDlookup = {v:k for k, v in AXID.items()}

    # write all variables to file corresponding to current ID
    currentIDstr = IDlookup[currentID]
    writeToFile( currentIDstr + '.txt' )

    # find file corresponding to target ID and load from it
    readBool = readFromFile( targetIDstr + '.txt' )

    if readBool:
        print("Axis change success!!")

    return


if __name__ == "__main__":
    debug=True

    # check args
    # if wrong arguments, exit with explanation
    if len(sys.argv) != 2: # sys.argv has arg 1 as the command itself
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is:")
        print("   ./changeAxisDogleg.py L#_DL#_A#")
        sys.exit()

    changeAxis(sys.argv[1])