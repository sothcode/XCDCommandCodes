#!/usr/bin/python3

from quickAssign import sendcommand
from quickReport import readback
import sys
import time
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from variableDictionaryXCD2 import varThetaSCommands as COMM
from changeAxisDogleg import changeAxis
#import random #for testing

#tuning settings
sleeptime=0.5 #in seconds
debug=False

#{later:
#get current rotations
#calculate destination nRotations
#if that's tolerable
#}

def _reverseLookup(dict,val):
    #set up the reverse dictionary
    reverse_mapping={v: k for k, v in dict.items()}
    try:
        key=reverse_mapping[val]
    except KeyError as e:
        print(f"errorCode lookup failed.  KeyError: {e}")
        sys.exit()
    return key  


def gotoThetaS(whereToGo):
    #check if controller is busy.  If so, exit with explanation
    if debug:
        print("goto:  Check status:")
    status=readback(ADDR['STATUS'])

    if status!=0:
        print("NOT EXECUTED. Controller status is not 0.")
        sys.exit()
    try:
        destination = float(whereToGo)
    except ValueError:
        print("Error: Not a valid number")
        sys.exit()

    sendcommand(COMM['GOTO'],destination) # this sleeps until it sees the status change from new_command

    #monitor the controller position and report at intervals of sleeptime
    if debug:
        print("goto:  Check position:");
    position=readback(ADDR['FPOS'])
    if debug:
        print("goto:  Check status:");
    status=STAT['BUSY']
    while status==STAT['BUSY']:
        status=readback(ADDR['STATUS'])
        print("position:",readback(ADDR['FPOS'])," status:",status)
        if debug:
            print ("goto: loop: check status:")
        status=readback(ADDR['STATUS'])
        time.sleep(sleeptime)

    #loop until controller busy flag is cleared

    #report final position and success
    if debug:
        print ("goto: finishing up.  check status and readback:")
    
    position=readback(ADDR['FPOS'])
    status=readback(ADDR['STATUS'])
    hb=readback(ADDR['HARD_STOP2'])
    lb=readback(ADDR['HARD_STOP1'])

    if status==STAT['READY']:
        print("SUCCESS. gotoThetaS complete.  status: %s (%s) position:%1.5f lb:%1.5f hb:%1.5f"%(status,_reverseLookup(STAT,status),position,lb,hb))
        return True, position
    else:
        print("FAIL. gotoThetaS failed.  status: %s (%s) position:%1.5f lb:%1.5f hb:%1.5f"%(status,_reverseLookup(STAT,status),position,lb,hb))
        return False, position


if __name__ == "__main__":
    #check args
    if len(sys.argv)==2:
        #keep current leg, assume arg is destination.
        inputval=sys.argv[1]
    elif len(sys.argv)==3:
        #assume first arg is leg, assume second arg is destination.
        changeAxis(sys.argv[1])
        inputval=sys.argv[2]
    else:
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is:")
        print("     ./gotoThetaS.py [position]")
        print("  or ./gotoThetaS.py L#_TH_S [position]")
        sys.exit()
    #if wrong arguments, exit with explanation
    
    gotoThetaS(inputval)