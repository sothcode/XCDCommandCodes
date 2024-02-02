#!/usr/bin/python3

from quickAssign import sendcommand
from quickReport import readback
import sys
import time
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from variableDictionaryXCD2 import varPhiCommands as COMM
from changeAxisDogleg import changeAxis
#import random #for testing

#tuning settings
sleeptime=0.5 #in seconds
debug=False


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
    print("     ./gotoPhi.py [position]")
    print("  or ./gotoPhi.py L#_PH [position]")
    sys.exit()
#if wrong arguments, exit with explanation

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
    destination = float(inputval)
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
    hardstop1=readback(ADDR['HARD_STOP1'])
    hardstop2=readback(ADDR['HARD_STOP2'])
    print("position:",readback(ADDR['FPOS'])," status:",status, "lb:",hardstop1, "hb:",hardstop2)
    if debug:
        print ("goto: loop: check status:")
    status=readback(ADDR['STATUS'])
    time.sleep(sleeptime)

#loop until controller busy flag is cleared

#report final position and success
if debug:
     print ("goto: finishing up.  check status and readback:")
if status==STAT['READY']:
    print("SUCCESS. gotoPhi complete.  status:",readback(ADDR['STATUS'])," position:{:.4g}".format(readback(ADDR['FPOS'])), \
          " lb:",readback(ADDR['HARD_STOP1']), " hb:",readback(ADDR['HARD_STOP2']));
else:
    print("FAIL. gotoPhi failed.  status:",readback(ADDR['STATUS'])," position:{:.4g}".format(readback(ADDR['FPOS'])), \
          " lb:",readback(ADDR['HARD_STOP1']), " hb:",readback(ADDR['HARD_STOP2']));

