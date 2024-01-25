#!/opt/homebrew/bin/python3
import quickAssign
import quickReport
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

#wrapper for the two-argument reportXCD2
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
status=readback(status_name)

if status==status_busy_value:
    print("NOT EXECUTED. Controller is busy.")
    sys.exit()


    
#set controller destination to the argument
writeXCD2([command_argument_name, destination])
#set the controller flag to move
writeXCD2([command_word_name,goto_command_value])

#monitor the controller position and report at intervals of sleeptime
position=readback(position_feedback_name)
status=readback(status_name)
while status==status_busy_value:
    print("position:",readback(position_feedback_name)," status:",status)
    status=readback(status_name)
    time.sleep(sleeptime)

#loop until controller busy flag is cleared

#report final position and success
print("DONE. gotoDogleg complete.  status:",readback(status_name)," position:",readback(position_feedback_name));

