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


def _reverseLookup(dict,val):
    #set up the reverse dictionary
    reverse_mapping={v: k for k, v in dict.items()}
    try:
        key=reverse_mapping[val]
    except KeyError as e:
        print(f"errorCode lookup failed.  KeyError: {e}")
        sys.exit()
    return key  


def clearDogleg():

    #check if controller is busy.  If so, exit with explanation
    if debug:
        print("clear:  Check status:")
    status=readback(ADDR['STATUS'])

    if status == 98:
        print("NOT EXECUTED.  Controller has boot status",status," (",_reverseLookup(STAT,status),").  setAxis.py must be run.")
        sys.exit()

    writeXCD2([ADDR['STATUS'], 0])
    writeXCD2([ADDR['COMMAND'], 0])
    new_status=readback(ADDR['STATUS'])
    print("DONE.  Dogleg status was ",status," (",_reverseLookup(STAT,status),"), is nowstatus:",new_status," (",_reverseLookup(STAT,new_status),").")


    return

if __name__ == "__main__":
    #check args
    if len(sys.argv) != 1: #note that sys.argv has arg 1 as the command itself
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is ./clearDogleg.py")
        sys.exit()
    clearDogleg()
    #if wrong arguments, exit with explanation