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

    with open(filename, "w") as file:
        # go thru varDict
        for varName, varVal in ADDR.items():

            # report every variable from varDict
            check, trueVal = reportXCD2([varVal])

            if check==False:
                print("CRITICAL FAILURE. Communication error.")
                sys.exit()
        
            if debug:
                print("_readback result: ", trueVal[0])
        
            # Logs the change to the log for a change
            file.write('%s %s\n' % (varName, trueVal[0]))


    return 


def readFromFile( filename ):

    if not os.path.isfile(filename):
        print("Couldn't read from file. Variables not updated.")
        return False

    with open(filename, "r") as file:
        for line in file:
            (varName, varVal) = line.split()

            writeXCD2([ADDR[varName], varVal])
        
    return True



def changeAxis( targetIDstr ):
    #check if controller is busy.  If so, exit with explanation
    if debug:
        print("changeAxis:  Check status:")

    #commenting out the status check, which causes failures if something is unplugged -- we're unable to switch away.
    #    print("before readback")
#    status=readback(ADDR['STATUS'])
#    print("after readback")
#    
#    if status!=0:
#        if status == 98.0:
#            print("Axis must be set by calling setAxis.py")
#
#        else:
#            print("NOT EXECUTED. Controller status is not 0.")
#            sys.exit()
#    print('about to look in AXID keys')
    # check if axis we want to change to is a valid motor, and if not exit
    if targetIDstr not in AXID.keys():
        print("Axis ID - " + targetIDstr + " -  not recognized. Axis ID list given as:")
        print(AXID.keys())
        return False

    # now find port corresponding to new axis 
    # first open port database file
    # print("about to query db")
    ret = kfDatabase.readVar(portsDb, targetIDstr)
    # print("kfDatabase returns %s"%ret)

    # exit if we don't have a port
    if ret[0] == False:
        print("Axis ID '%s' not found in database '%s'.  Run updatePorts.py." % (targetIDstr, portsDb))
        return False

    # before we go, save the old FPOS and nturns, just in case:
    oldID=readback(ADDR['ID'])
    oldAxis=readback(ADDR['XAXIS'])
    oldStatus=readback(ADDR['STATUS'])
    oldPos=readback(ADDR['FPOS'])
    oldTurns=readback(ADDR['TURNS'])
        
    # otherwise, assign new port to targetPort
    targetPort = ret[1][0]
    targetAxis = ret[1][1]
   # (this will change to object in class when we refactor)
    if not (os.path.exists(PORTFILE)):
        print("PORTFILE %s does not exist.  PANIC" % PORTFILE)
        sys.exit()
    
    # if PORTFILE exists, load in old port and set active port
    # with open(PORTFILE, 'r') as file:
    #     oldPort = file.readline()
    with open(PORTFILE, 'w') as file:
        file.write(targetPort)

    
    # readback current axis and current axis ID and find target axis ID
    # currentID = readback(ADDR['ID'])
    # targetID = AXID[targetIDstr]
    # oldAxis = readback(ADDR['XAXIS'])
    currentAxis = readback(ADDR['XAXIS'])
    
    # check if current ID and target ID are the same
    if (currentAxis == targetAxis):
        print("changeAxis: XAXIS is the same.  Values remain from last use, not loaded from file.")
        return

    # newAxis = readback(ADDR['XAXIS'])
    # if oldAxis == newAxis:
    #     print("changeAxis: Port changed but axis unchanged. Variables not updated.")
    #     return

    # create lookup table of axis variables
    IDlookup = {v:k for k, v in AXID.items()}

    # write all variables to file corresponding to current ID
    currentID = readback(ADDR['ID'])
    currentIDstr = IDlookup[currentID]
    writeToFile( currentIDstr + '.txt' )

    # find file corresponding to target ID and load from it
    readBool = readFromFile( targetIDstr + '.txt' )

    # now read the current state:
    newID=readback(ADDR['ID'])
    newAxis=readback(ADDR['XAXIS'])
    newStatus=readback(ADDR['STATUS'])
    newPos=readback(ADDR['FPOS'])
    newTurns=readback(ADDR['TURNS'])

    
    if readBool:
        print("changeAxis: Axis changed to '%s' on port '%s'"% (targetIDstr, targetPort))
    else:
        print("FAILURE: changeAxis: Axis could not be changed to '%s' on port '%s'"% (targetIDstr, targetPort))
    print("was: %s pos=%s, axis=%s, stat=%s, turns=%s"%(IDlookup[oldID],oldPos,oldAxis,oldStatus,oldTurns)) 
    print("now: %s pos=%s, axis=%s, stat=%s, turns=%s"%(IDlookup[newID],newPos,newAxis,newStatus,newTurns)) 
        
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



# success, targetPort, targetAxis = changeAxis( axisName )


# change axis does the following
# 1) checks if targetIDstr (i.e. axisName) is in ID_dict.keys()
# 2) looks up axisName in kfDatabase
# 3) if ret[0]/success is False, print axis not found
# 4) extracts target port and axis from ret (same as value[0], value[1])
# 5) check if portfile exists, and if so, write target port from kfdb
# 6) readback current XAXIS
# 7) if XAXIS same values remain from last use and return
# 8) otherwise create lookup table from ID_dict and find ID corresponding to current axis
# 9) write values from current axis to file
# 10) read from file values corresponding to current axis
# 11) print report of what changed