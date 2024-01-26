#!/usr/bin/python3

from quickAssign import sendcommand
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

if len(sys.argv) != 2: #note that sys.argv has arg 1 as the command itself
    print("NOT EXECUTED. Wrong number of arguments.  Correct usage is ./gotoDogleg.py [position]")
    sys.exit()
#if wrong arguments, exit with explanation
destination=sys.argv[1]

#{later:
#get current rotations
#calculate destination nRotations
#if that's tolerable
#}

#check if controller is busy.  If so, exit with explanation
if debug:
    print("goto:  Check status:")
status=readback(ADDR['STATUS'])

if status!=0:
    print("NOT EXECUTED. Controller status is not 0.")
    sys.exit()
try:
    input = float(sys.argv[1])
except ValueError:
    print("Error: Not a valid number")
    sys.exit()

sendcommand(COMM['GOTO'],input) # this sleeps until it sees the status change from new_command

#monitor the controller position and report at intervals of sleeptime
if debug:
    print("goto:  Check position:");
position=readback(ADDR['FPOS'])
if debug:
    print("goto:  Check status:");
status=status_busy_value
while status==status_busy_value:
    status=readback(ADDR['STATUS'])
    turns=readback(ADDR['TURNS'])
    print("position:",readback(ADDR['FPOS'])," status:",status, "turns:",turns)
    if debug:
        print ("goto: loop: check status:")
    status=readback(ADDR['STATUS'])
    time.sleep(sleeptime)

#loop until controller busy flag is cleared

#report final position and success
if debug:
     print ("goto: finishing up.  check status and readback:")
if status==status_ready_value:
    print("SUCCESS. gotoDogleg complete.  status:",readback(ADDR['STATUS'])," position:",readback(ADDR['FPOS']), "nTurns:",readback(ADDR['TURNS']);
else:
    print("FAIL. gotoDogleg failed.  status:",readback(ADDR['STATUS'])," position:",readback(ADDR['FPOS']), "nTurns:",readback(ADDR['TURNS']);

