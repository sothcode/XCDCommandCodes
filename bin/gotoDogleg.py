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
    return ret[0]

def sendcommand(com,arg):
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
        print("command: set arguement:")    
    writeXCD2([command_argument_name, arg)    
   if debug:
        print("command: set status to new_command:")    
    writeXCD2([command_argument_name, arg)    
    #set the command byte last, so we know we don't have a race condition
    if debug:
        print("command: set command byte:")    
    writeXCD2([command_word_name,com])

    #now wait until the status changes to indicate the command has been acted on:
    status=readback(status_name)
    while status==status_new_command_value:
        if debug:
            print ("command: waiting for device to ack command:")
        status=readback(status_name)
        time.sleep(sleeptime)

    return
    


#variable names we need
position_feedback_name="FPOS"
status_name="V19"
command_word_name="V0"
command_argument_name="V10"

#variable values we need
goto_command_value=6
status_busy_value=9
status_received_value=8

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
    status=readback(status_name)

if status==status_busy_value:
    print("NOT EXECUTED. Controller is busy.")
    sys.exit()
try:
    input = float(sys.argv[1])
except ValueError:
    print("Error: Not a valid number")
    sys.exit()

sendcommand(goto_command_value,input) # this sleeps until it sees the status change from new_command

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

