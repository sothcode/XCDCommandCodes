#!/bin/python3
import math
import sys
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR

debug=False

def changeAxis( targetIDstr ):
    if debug:
        print("(dummy) change axis to %s"%(targetIDstr))
    return

def sendcommand(com,arg):
    if debug:
        print("(dummy) send command [%s,%s]"%(com,arg))
    return True

def writeXCD2(arg):
    if debug:
        print("(dummy) writeXCD2 %s"%arg)
    return

def readback(arg):
    legibleArg=_reverseLookup(ADDR,arg)
    if not hasattr(readback, "callList"):
        readback.callList = {}
    val=readback.callList.get(arg,0)
    readback.callList[arg]=val+1
    count=readback.callList[arg]
    ret=0
    if legibleArg=='COMMAND' or legibleArg=='ID':
        ret = 101
    elif legibleArg=='HARD_STOP1':
        ret = -4.5
    elif legibleArg=='HARD_STOP2':
        ret=4.5
    elif legibleArg=='TURNS':
        ret = int(math.sin(count/10)*3)*1.0  #oscillates between -3 and +3
    elif legibleArg=='STATUS': #say busy for a while, then say 'ready'.
        if count>10 or count<2:
            ret=0
        else:
            ret=9
    elif legibleArg=='FPOS':
        ret = math.sin(count/10)*3  #oscillates between -3 and +3
    elif legibleArg=='ENR':
        ret=0.00006125
    elif legibleArg=='XAXIS':
        ret=1.0
    else:
        print("(dummy) No set behavior for arg=%s(%s).  Returning 0.0"%(arg,legibleArg))
    
    if debug:
        print("(dummy) readback [%s]"%(arg))
    return ret


def _reverseLookup(dict,val):
    #set up the reverse dictionary
    reverse_mapping={v: k for k, v in dict.items()}
    try:
        key=reverse_mapping[val]
    except KeyError as e:
        print("address lookup failed.  KeyError: %s"%(e))
        sys.exit()
    return key

