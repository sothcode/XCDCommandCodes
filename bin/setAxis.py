#!/usr/bin/python3

import sys
import os
from quickReport import readback
from quickAssign import writeXCD2
from changeAxisDogleg import readFromFile, writeToFile
import clearDogleg as clearDogleg
from variableDictionaryXCD2 import varDict
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from variableDictionaryXCD2 import varDoglegCommands as COMM
from variableDictionaryXCD2 import varUniqueID as AXID
#import random #for testing

#tuning settings
sleeptime=0.5 #in seconds
debug=False



def setAxis( axisStr ):
    
    #check if controller is busy.  If so, exit with explanation
    if debug:
        print("setAxis:  Check status:")
    status=readback(ADDR['STATUS'])

    if axisStr not in AXID.keys():
        print("Axis ID - " + axisStr + " -  not recognized. Axis ID list given as:")
        print(AXID.keys())
        sys.exit()

    # first write all current values to junk file that can be overwritten
    writeToFile('junk.txt')

    # then, if file corresponding to newAxis exists, load values
    readBool = readFromFile( axisStr + '.txt' )

    if readBool:
        print("Axis set successfully.")        
        writeXCD2([ADDR['COMMAND'], 0])
        writeXCD2([ADDR['STATUS'], 0])
        new_status=readback(ADDR['STATUS'])
        print("DONE.  Status was",status, ",is now",new_status)


    return


if __name__ == "__main__":
    debug=True

    # check args
    # if wrong arguments, exit with explanation
    if len(sys.argv) != 2: # sys.argv has arg 1 as the command itself
        print("NOT EXECUTED. Inserted argument when not needed.")
        sys.exit()

    setAxis(sys.argv[1])


'''
 if status!=98:
        print("NOT EXECUTED. setAxis can only be called upon startup when controller has status 98.")
        sys.exit()
'''