#!/usr/bin/python3

from quickAssign import sendcommand, writeXCD2
from quickReport import readback
import sys
import time
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from variableDictionaryXCD2 import varDoglegCommands as COMM
#import random #for testing

#tuning settings
sleeptime=0.5 #in seconds
debug=False


#check args

if len(sys.argv) != 1: #note that sys.argv has arg 1 as the command itself
    print("NOT EXECUTED. Wrong number of arguments.  Correct usage is ./clearDogleg.py")
    sys.exit()
#if wrong arguments, exit with explanation

#check if controller is busy.  If so, exit with explanation
if debug:
    print("clear:  Check status:")
status=readback(ADDR['STATUS'])
writeXCD2([ADDR['STATUS'], 0])
new_status=readback(ADDR['STATUS'])
print("DONE.  Dogleg status was",status, ",is now",new_status)
