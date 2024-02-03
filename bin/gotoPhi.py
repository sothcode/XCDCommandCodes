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
timeout = 10    # in seconds
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

def gotoPhi( whereToGo ):

    #check if controller is busy.  If so, exit with explanation
    if debug:
        print("goto:  Check status:")
    status=readback(ADDR['STATUS'])

    if status!=0:
        print("NOT EXECUTED. Controller status is not 0.")
        return False, 0
    try:
        destination = float(whereToGo)
    except ValueError:
        print("Error: Not a valid number")
        return False, 0

    commandSent=sendcommand(COMM['GOTO'],destination) # this sleeps until it sees the status change from new_command
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
    axis=readback(ADDR['XAXIS'])
    hardstop1=readback(ADDR['HARD_STOP1'])
    hardstop2=readback(ADDR['HARD_STOP2'])
    t1=time.time()
    while status==STAT['BUSY']  and (time.time()-t1) < timeout:
        oldposition=position
        position=readback(ADDR['FPOS'])
        turns=readback(ADDR['TURNS'])
        print("position:%s status:%s (%s) turns:%s (not live: lb:%1.4f hb:%1.4f)"%(position,status,_reverseLookup(STAT,status),turns,hardstop1,hardstop2))
        if debug:
            print ("goto: loop: check status:")
        status=readback(ADDR['STATUS'])
        time.sleep(sleeptime)
        
        turns=readback(ADDR['TURNS'])
        print("position:", position," (axis",axis,") status:",status," (",_reverseLookup(STAT,status),") turns:",turns)
        if debug:
            print ("goto: loop: check status:")

        # sleep a little, and if same position, enter timeout loop
        time.sleep(sleeptime)
        
        # check that we're moving
        if abs(position-oldposition) > 3*readback('ENR'):
            t1 = time.time()

        # otherwise update status and continue
        status=readback(ADDR['STATUS']) 

    if status==STAT['BUSY']: #this occurs if we leave the loop due to timeout rather than status change
        writeXCD2([ADDR['STATUS'], 80])
        time.sleep(sleeptime)

    #loop until controller busy flag is cleared

    #report final position and success
    if debug:
        print ("goto: finishing up.  check status and readback:")


    #report final position and success
    if debug:
        print ("goto: finishing up.  check status and readback:")
    position=readback(ADDR['FPOS'])
    status=readback(ADDR['STATUS'])
    hb=readback(ADDR['HARD_STOP2'])
    lb=readback(ADDR['HARD_STOP1'])

    if status==STAT['READY']:
        print("SUCCESS. gotoPhi complete.  status: %s (%s) position:%1.5f lb:%1.5f hb:%1.5f"%(status,_reverseLookup(STAT,status),position,lb,hb))
        return True, position
    else:
        print("FAIL. gotoPhi failed.  status: %s (%s) position:%1.5f lb:%1.5f hb:%1.5f"%(status,_reverseLookup(STAT,status),position,lb,hb))
        return False, position




if __name__ == "__main__":
    #check args
    if len(sys.argv)==2:
        #keep current leg, assume arg is destination.
        inputval=sys.argv[1]
        #printf("NOT EXECUTED. Must specify an axis and a destination, now.")
        #sys.exit()
    elif len(sys.argv)==3:
        #assume first arg is leg, assume second arg is destination.
        #get its port from the db
        changeAxis(sys.argv[1])
        inputval=sys.argv[2]
    else:
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is:")
        print("     ./gotoPhi.py [position]")
        print("  or ./gotoPhi.py L#_PH [position]")
        sys.exit()
    #if wrong arguments, exit with explanation

    gotoPhi(inputval)

