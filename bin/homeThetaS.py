#!/usr/bin/python3

from quickAssign import sendcommand, writeXCD2
from quickReport import readback
import sys
import time
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from variableDictionaryXCD2 import varThetaSCommands as COMM
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
        print("reverse lookup failed.  KeyError: %s"%(e))
        sys.exit()
    return key


#check args

if len(sys.argv) != 1: #note that sys.argv has arg 1 as the command itself
    print("NOT EXECUTED. Wrong number of arguments.  Correct usage is ./homeThetaS.py")
    sys.exit()
#if wrong arguments, exit with explanation

#check if controller is busy.  If so, exit with explanation
if debug:
    print("goto:  Check status:")
status=readback(ADDR['STATUS'])

if status!=0:
    print("NOT EXECUTED. Controller status is not 0.")
    sys.exit()


sendcommand(COMM['HOME'],0) # this sleeps until it sees the status change from new_command

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
    print ("homeThetaS: finishing up.  check status and readback:")

print("Setting current position to home.  Offset was %s from previous home"%position)
writeXCD2([ADDR['FPOS'], 0])
lb=readback(ADDR['HARD_STOP1'])
hb=readback(ADDR['HARD_STOP2'])
position=readback(ADDR['FPOS'])   
turns=readback(ADDR['TURNS'])
axis=readback(ADDR['XAXIS'])   

if status==STAT['READY']:
    print("SUCCESS. homeThetaS complete. status: %s (%s) position:%1.6f axis:%s turns:%s lb:%1.5f hb:%1.5f"%(status,_reverseLookup(STAT,status),position,axis, turns,lb,hb))
else:
    print("FAIL. homeThetaS failed. status: %s (%s) position:%1.6f axis:%s turns:%s lb:%1.5f hb:%1.5f"%(status,_reverseLookup(STAT,status),position,axis, turns,lb,hb))    
