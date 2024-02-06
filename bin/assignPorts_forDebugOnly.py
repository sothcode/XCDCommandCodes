#!/bin/python3

# a quick function to set the UARTS on ttyUSB0 and ttyUSB1 so that updatePorts sees two doglegs.
from quickAssign import writeXCD2
from quickReport import readback
import sys
import time
from variableDictionaryXCD2 import varUniqueID as ID
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT


#tuning settings
sleeptime=0.5 #in seconds
debug=False

def _reverseLookup(dict,val):
    #set up the reverse dictionary
    reverse_mapping={v: k for k, v in dict.items()}
    try:
        key=reverse_mapping[val]
    except KeyError as e:
        print("reverse lookup failed.  KeyError: %s"%(e))
        sys.exit()
    return key



if __name__ == "__main__":

    #check args
    #note that sys.argv has arg 1 as the command itself
    if len(sys.argv) != :
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is ./assignPorts[tab]")
        sys.exit()
    #if wrong arguments, exit with explanation

    #check if controller is busy.  If so, exit with explanation
    if debug:
        print("clear:  Check status:")



    status=readback(ADDR['STATUS'])
    axis=readback(ADDR['XAXIS'])

    writeXCD2([ADDR['XAXIS'], sys.argv[1]])
    writeXCD2([ADDR['STATUS'], 0])
    writeXCD2([ADDR['COMMAND'], 0])
    new_status=readback(ADDR['STATUS'])
    new_axis=readback(ADDR['XAXIS'])
    print("Done.  ax=%s, status %s (%s) ==> ax=%s, status %s (%s)"%(axis,status,_reverseLookup(STAT,status),new_axis,new_status,_reverseLookup(STAT,new_status)))


    writeXCD2(['UART0_ADDRESS', ID['DEBUG0_DL0_A0']])
    writeXCD2(['UART1_ADDRESS', ID['DEBUG0_DL0_A1']])
    writeXCD2(['UART0_ADDRESS', ID['DEBUG0_DL1_A0']])
    writeXCD2(['UART1_ADDRESS', ID['DEBUG0_DL1_A1']])