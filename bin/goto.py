#!/usr/bin/python3

# This is designed to tell a particular named motor axis to go to a particular named position.
# To prevent alignment accidents, it will not send a dogleg to a numeric position.  for that, you need to use gotoDogleg
# If the axis is not connected, or the requested named position is not in the database, it fails.

from quickAssign import sendcommand,writeXCD2
from quickReport import readback
#from dummySerial import sendcommand,readback,changeAxis
import sys
import re
import time
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from variableDictionaryXCD2 import varAllCommands as ALL_COMM
from changeAxisDogleg import changeAxis

# to load tty data from the db so we know which tty we want:
sys.path.append("kfDatabase")
import kfDatabase

#tuning settings
sleeptime=0.6 #in seconds
timeout=10
debug=True
#portsDb="xcd2_ports.kfdb"
#mainDb="axis_parameters.kfdb"
portsDb="test_only_xcd2_ports.kfdb"
mainDb="test_only_axis_parameters.kfdb"
PORTFILE="XCD_current_port"


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

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def find_comm(axisName):
    #return a command lookup table matching the axis.
    #also let us know if the axis is a dogleg, so we know how to behave.
    isDogleg=False
    COMM={}
    if bool(re.match(r'^.+_DL\d_A\d$',axisName)):
        COMM=ALL_COMM['Dogleg']
        isDogleg=True
    elif bool(re.match(r'^.+_TH_S$',axisName)):
        COMM=ALL_COMM['ThetaS']
    elif bool(re.match(r'^.+_TH_L$',axisName)):
        COMM=ALL_COMM['ThetaL']
    elif bool(re.match(r'^.+_PH$',axisName)):
        COMM=ALL_COMM['Attenuator']        
    elif bool(re.match(r'^.+_PH$',axisName)):
        COMM=ALL_COMM['Attenuator']
    else:
        print("no match of '%s' to axis types.  Critical failure!"%(axisName))
        sys.exit()
    return isDogleg, COMM
    
def goto( axisName=None, destination=None):
    if axisName==None or destination==None:
        print("wrong args for goto.  requires two arguments.")
        return False
    
    #check if that axis is connected.  Fail if not
    success, value=kfDatabase.readVar(portsDb,axisName)
    if not success:
        print("goto: kfDatabase failed.  Axis '%s' not connected. (or port database is stale)" % axisName)
        return False
    targetPort,targetAxis=value[0],value[1]
    
    #set command lookup table to match the axis
    isDogleg,COMM=find_comm(axisName)
    
    #check to see if the target is a number.
    #if number: make it a float.
    if (is_number(destination)):
        targetPos=float(destination) # we handle the dogleg condition below.
            
    #if not number: open the dictionary and see if that axis has that variable set.  Fail if not
    else:
        #  get the value from the dict.
        keyName=axisName+"/"+str(destination)
        if debug:
            print("goto: looking for value %s"%keyName)
        success,value=kfDatabase.readVar(mainDb, keyName)
        if not success:
            print("goto: kfDatabase failed.  destination '%s' not found for %s. (kfdb=%s, key=%s)" % (destination,axisName,mainDb,keyName))
            return False        
        #  check to see if the dict value is a number.
        #  if number: make it a float.
        if (is_number(value)):
            targetPos=float(value)
        else:
            print("goto: kfDatabase key '%s' has non-numeric value %s" % (keyName,str(value)))
            return False

    #refuse to move if we are asking a dogleg to move to a numeric position (to prevent accidents)
    if isDogleg and is_number(destination):
        print("goto: refused.  To prevent breaking alignment by accident, you must use gotoDogleg, not goto, to move '%s' to '%s'."%(axisName,destination))
        return
    
    #now we are guaranteed we have a reachable axis, and a target position as a float.
    #we are also guaranteed that we are not moving a dogleg to a numeric position.

    #set the current port through the file:
    with open(PORTFILE,'w') as file:
        file.write(targetPort)
    #changeAxis:
    writeXCD2([ADDR['XAXIS'],0])
    
    #check if controller is busy.  If so, exit with explanation
    if debug:
        print("goto:  Check status:")
    status=readback(ADDR['STATUS'])

    if status!=0:
        print("NOT EXECUTED. Controller status is not 0. status: %s (%s)"%(status,_reverseLookup(STAT,status)))
        return False, 0
    
    print("goto: sending command %s",COMM['GOTO'])
    commandSent=sendcommand(COMM['GOTO'],targetPos) # this sleeps until it sees the status change from new_command
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
        print("SUCCESS. goto %s %s complete.  status: %s (%s)"%(axisName, destination ,status, _reverseLookup(STAT,status))," position:{:.4g} (ax{:.1g})".format(readback(ADDR['FPOS']),readback(ADDR['XAXIS'])), "nTurns:",readback(ADDR['TURNS']));
        return True, lastpos
    
    print("FAIL. goto %s %s failed.  status: %s (%s)"%(axisName, destination ,status, _reverseLookup(STAT,status))," position:{:.4g} (ax{:.1g})".format(readback(ADDR['FPOS']),readback(ADDR['XAXIS'])), "nTurns:",readback(ADDR['TURNS']));
    return False, lastpos




if __name__ == "__main__":
    #check args
    if len(sys.argv)==3:
        #assume first arg is leg, assume second arg is destination.
        #get its port from the db
        axis=sys.argv[1]
        dest=sys.argv[2]
    else:
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is:")
        print("   ./goto.py laser_name position")
        sys.exit()
    #if wrong arguments, exit with explanation

    goto(axis,dest)
