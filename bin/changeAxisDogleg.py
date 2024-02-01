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

# to load tty data from the db so we know which tty we want:
sys.path.append("kfDatabase")
import kfDatabase


# tuning settings
sleeptime=0.5 #in seconds
debug=False
portsDb="xcd2_ports.kfdb"
PORTFILE="XCD_current_port"



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

    # check if axis we want to change to is a valid axis, and if not exit
    if targetIDstr not in AXID.keys():
        print("Axis ID - " + targetIDstr + " -  not recognized. Axis ID list given as:")
        print(AXID.keys())
        sys.exit()


    
    # now find port corresponding to new axis 
    # first open port database file
    ret = kfDatabase.readVar(portsDb, targetIDstr)

    # exit if we don't have a port
    if ret[0] == False:
        print("Axis ID '%s' not found in database '%s'.  Run updatePorts.py." % (targetIDstr, portsDb))
        sys.exit()

    # otherwise, assign new port to targetPort
    targetPort = ret[1][0]

    # check which serial port we were using - can be found in PORTFILE
    # (this will change to object in class when we refactor)
    oldPort = None
    if not (sys.path.exists(PORTFILE)):
        print("PORTFILE %s does not exist.  PANIC" % PORTFILE)
        sys.exit()
    
    # if PORTFILE exists, load in old port and set active port
    with open(PORTFILE, 'r') as file:
        oldPort = file.readline()
    with open(PORTFILE, 'w') as file:
        file.write(targetPort)

    # readback current axis and find target axis IDs
    currentID = readback(ADDR['ID'])
    targetID = AXID[targetIDstr]

    # check if current axis and target axis are the same
    if (currentID == targetID) and (oldPort==targetPort):
        print("changeAxis: Port and Laser ID are already correct.")
        return

    # create lookup table of axis variables
    IDlookup = {v:k for k, v in AXID.items()}

    # write all variables to file corresponding to current ID
    currentIDstr = IDlookup[currentID]
    writeToFile( currentIDstr + '.txt' )

    # find file corresponding to target ID and load from it
    readBool = readFromFile( targetIDstr + '.txt' )

    if readBool:
        print("changeAxis: Axis changed to '%s' on port '%s'"% (targetIDstr, targetPort))
    else:
        print("FAILURE: changeAxis: Axis could not be changed to '%s' on port '%s'"% (targetIDstr, targetPort))

    return


if __name__ == "__main__":
    # check args
    # if wrong arguments, exit with explanation
    if len(sys.argv) == 2: # sys.argv has arg 1 as the command itself
        changeAxis(sys.argv[1])
    elif len(sys.argv)==3 and sys.argv[2]==1:
        debug=True
        changeAxis(sys.argv[1])
    else:
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is:")
        print("   ./changeAxisDogleg.py L#_DL#_A#")
        print("or turn on debug with   ./changeAxisDogleg.py L#_DL#_A# 1")
        sys.exit()
