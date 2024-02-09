#!/bin/python3

# a quick function to set the UARTS on ttyUSB0 and ttyUSB1 so that updatePorts sees two doglegs.
from quickAssign import writeXCD2
from quickReport import readback
from xcdSerial import getCurrentPort
import sys
import time
from variableDictionaryXCD2 import varUniqueID as ID
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT


#tuning settings
sleeptime=0.5 #in seconds
debug=False
PORTFILE="XCD_current_port"


def _reverseLookup(dict,val):
    #set up the reverse dictionary
    reverse_mapping={v: k for k, v in dict.items()}
    try:
        key=reverse_mapping[val]
    except KeyError as e:
        print("reverse lookup failed.  KeyError: %s"%(e))
        sys.exit()
    return key

def assignUARTsToPort(port, id0, id1):
    print("assigning %s:  ax0:%s ax1:%s"%(port,id0,id1))
    port_before=getCurrentPort()
    with open(PORTFILE, 'w') as file:
        file.write(port)
    writeXCD2(['UART0_ADDRESS', id0])
    writeXCD2(['UART1_ADDRESS', id1])    
    with open(PORTFILE, 'w') as file:
        file.write(port_before)


if __name__ == "__main__":

    #check args
    #note that sys.argv has arg 1 as the command itself
    #if wrong arguments, exit with explanation
    if len(sys.argv) == 1: #overall default
        print("Assigning to ttyUSB0 and USB1 to default dogleg assumption:")
        assignUARTsToPort("/dev/ttyUSB0", ID['DEBUG_DL0_A1'], ID['DEBUG_DL0_A0'])
        assignUARTsToPort("/dev/ttyUSB1", ID['DEBUG_DL1_A1'], ID['DEBUG_DL1_A0'])
    elif len(sys.argv)==2: #allow two possibilities:  'doglegs' or 'egg'.  do the default assumption for those.
        if sys.argv[2]='doglegs':
            print("Assigning to ttyUSB0 and USB1 to default dogleg assumption:")
            assignUARTsToPort("/dev/ttyUSB0", ID['DEBUG_DL0_A1'], ID['DEBUG_DL0_A0'])
            assignUARTsToPort("/dev/ttyUSB1", ID['DEBUG_DL1_A1'], ID['DEBUG_DL1_A0'])
        elif sys.argv[2]='egg':
            print("Assigning to ttyUSB0 and USB1 to default egg assumption:")
            assignUARTsToPort("/dev/ttyUSB0", ID['DEBUG_TH_L'], ID['DEBUG_TH_S'])
            assignUARTsToPort("/dev/ttyUSB1", ID['DEBUG_AT'], ID['DEBUG_PH'])
        else:
            print("no default assumption for '%s'.  Args are either 'doglegs' of 'egg'")
            sys.exiit()
    elif len(sys.argv)==3:
        port=sys.argv[1]
        idstr={}
        idnum={}
        for i in range(0,1)
            idstr[i]=sys.argv[i+2]
            idnum[i]=ID[idstr[i]]
        print("Assigning %s with UARTS %s(%s) and %s(%s)"%(port,idstr[0],idnum[0],idstr[1],idnum[1]))
        assignUARTsToPort(port,idnum[0],idnum[1])
    else:
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is ./assignPorts[tab] [doglegs/egg] or ./assignPorts[tab] port,  name0, name1")        
        sys.exit()
     
    print("Done.")
