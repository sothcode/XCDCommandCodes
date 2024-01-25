#!/usr/bin/python3
from quickAssign import writeXCD2
from quickReport import reportXCD2
import sys
import time
#import random #for testing

#temp:
#def writeXCD2(argv):
#    print("write",argv[0],argv[1])
#    return
#def reportXCD2(argv):
#    print("read",argv[0])
#    ret=random.randint(0, 100)
#    if ret>8:
#        return True, 9
#    return True, ret

#wrapper for the two-returns reportXCD2
def readback(arg):
    check,ret = reportXCD2([arg])
    if check==False:
        print("CRITICAL FAILURE. Communication error.")
        sys.exit()
    return ret


#variable names we need
position_feedback_name="FPOS"
status_name="V19"
command_word_name="V0"
command_argument_name="V10"

#variable values we need
goto_command_value=6
status_busy_value=9

#tuning settings
sleeptime=0.5 #in seconds
debug=True

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
    status=readback(status_name)

if status==status_busy_value:
    print("NOT EXECUTED. Controller is busy.")
    sys.exit()
try:
    input = float(sys.argv[1])
except ValueError:
    print("Error: Not a valid number")
    sys.exit()

if debug:
    print("goto:  Set destination:")    
#set controller destination to the argument
writeXCD2([command_argument_name, input])
#set the controller flag to move
if debug:
    print("goto:  Set command 'move':")    
writeXCD2([command_word_name,goto_command_value])

#monitor the controller position and report at intervals of sleeptime
if debug:
    print("goto:  Check position:");
position=readback(position_feedback_name)
if debug:
    print("goto:  Check status:");
status=readback(status_name)
while status==status_busy_value:
    print("position:",readback(position_feedback_name)," status:",status)
    if debug:
        print ("goto: loop: check status:")
    status=readback(status_name)
    time.sleep(sleeptime)

#loop until controller busy flag is cleared

#report final position and success
if debug:
     print ("goto: finishing up.  check status and readback:")
print("DONE. gotoDogleg complete.  status:",readback(status_name)," position:",readback(position_feedback_name));

