#!/usr/bin/python3

import sys
from quickAssign import sendcommand
from quickReport import readback
from variableDictionaryXCD2 import varDict
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from variableDictionaryXCD2 import varDoglegCommands as COMM
#import random #for testing

#tuning settings
sleeptime=0.5 #in seconds
debug=False


# check args
# if wrong arguments, exit with explanation
if len(sys.argv) != 1: # sys.argv has arg 1 as the command itself
    print("NOT EXECUTED. Inserted argument when not needed.")
    sys.exit()


#check if controller is busy.  If so, exit with explanation
if debug:
    print("goto:  Check status:")
status=readback(ADDR['STATUS'])

if status!=0:
    print("NOT EXECUTED. Controller status is not 0.")
    sys.exit()




print("Please enter filename to write current axis XAXIS=", XAXIS , "variables to.")