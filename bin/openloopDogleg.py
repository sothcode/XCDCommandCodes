#! /usr/bin/python3

from quickAssign import sendcommand, writeXCD2
from quickReport import readback
import sys
import time
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from variableDictionaryXCD2 import varDoglegCommands as COMM
from changeAxisDogleg import changeAxis

#tuning settings
sleeptime = 0.1 # in seconds
timeout = 10
debug = False

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
        print(f"gotoDogleg lookup failed.  KeyError: {e}")
        sys.exit()
    return key  

def openloopDogleg(time, PWM):

    #check if controller is busy.  If so, exit with explanation
    if debug:
        print("goto:  Check status:")

    status=readback(ADDR['STATUS'])
    if status!=0:
        print("NOT EXECUTED. Controller status is not 0.")
        return False, 0
    
    try:
        duration = float(time)
    except ValueError:
        print("Error: Not a valid number for duration to pulse drive signal.")
        return False, 0
    
    writeXCD2(['V6', duration])
    
    try:
        intensity = float(PWM)
    except ValueError:
        print("Error: Not a valid number for PWM intensity.")
        return False, 0

    commandSent=sendcommand(COMM['OPENLOOP'], intensity) # this sleeps until it sees the status change from new_command
    if not commandSent:
        return False, readback(ADDR['FPOS'])
    
    #monitor the controller position and report at intervals of sleeptime
    if debug:
        print("goto:  Check position:");
    position=readback(ADDR['FPOS'])
    if debug:
        print("goto:  Check status:");
    #status=STAT['BUSY']
    status=readback(ADDR['STATUS'])

    # while status is busy, print to screen position, axis, status and nTurns
    t1=time.time()
    while status==STAT['BUSY']  and (time.time()-t1) < timeout:
        axis=readback(ADDR['XAXIS'])
        turns=readback(ADDR['TURNS'])
        position=readback(ADDR['FPOS'])
        print("position:", position," (axis",axis,") status:",status," (",_reverseLookup(STAT,status),") turns:",turns)
        if debug:
            print ("goto: loop: check status:")

        # sleep a little, and if same position, enter timeout loop
        time.sleep(sleeptime)

        # check 
        if abs(readback(ADDR['FPOS'])-position) > 3*readback('ENR'):
            t1 = time.time()

        # otherwise update status and continue
        status=readback(ADDR['STATUS']) 

    if status==STAT['BUSY']:
        writeXCD2([ADDR['STATUS'], 80])
        time.sleep(sleeptime)

    #loop until controller busy flag is cleared

    #report final position and success
    if debug:
        print ("goto: finishing up.  check status and readback:")

    #status=readback(ADDR['STATUS'])  this is already read in the way we left the while loop above.
    lastpos=readback(ADDR['FPOS'])
    if status==STAT['READY']:
        print("SUCCESS. gotoDogleg complete.  status:",status," (", _reverseLookup(STAT,status),") position:{:.4g} (ax{:.1g})".format(readback(ADDR['FPOS']),readback(ADDR['XAXIS'])), "nTurns:",readback(ADDR['TURNS']));
        return True, lastpos
    
    print("FAIL. openloopDogleg failed.  status:",status," (", _reverseLookup(STAT,status),") position:{:.4g} (ax{:.1g})".format(readback(ADDR['FPOS']),readback(ADDR['XAXIS'])), "nTurns:",readback(ADDR['TURNS']));
    return False, lastpos

if __name__ == "__main__":
    if len(sys.argv) == 3:
        duration = sys.argv[1]
        intensity = sys.argv[2]
        openloopDogleg(duration, intensity)
    else:
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is:")
        print("     ./openloopDogleg.py [duration] [intensity]")
        sys.exit()