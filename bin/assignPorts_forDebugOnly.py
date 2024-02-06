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



if __name__ == "__main__":

    #check args
    #note that sys.argv has arg 1 as the command itself
    if len(sys.argv) != 1:
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is ./assignPorts[tab]")
        sys.exit()
    #if wrong arguments, exit with explanation


    port_before=getCurrentPort()
    with open(PORTFILE, 'w') as file:
        file.write("/dev/ttyUSB0")
    writeXCD2(['UART0_ADDRESS', ID['DEBUG_DL0_A0']])
    writeXCD2(['UART1_ADDRESS', ID['DEBUG_DL0_A1']])
    writeXCD2(['XAXIS',0])
    writeXCD2([ADDR['ID'], ID['DEBUG_DL0_A0']])
    with open(PORTFILE, 'w') as file:
        file.write("/dev/ttyUSB1")   
    writeXCD2(['UART0_ADDRESS', ID['DEBUG_DL1_A0']])
    writeXCD2(['UART1_ADDRESS', ID['DEBUG_DL1_A1']])
    writeXCD2(['XAXIS',0])
    writeXCD2([ADDR['ID'], ID['DEBUG_DL1_A0']])
    port_before=getCurrentPort()
    with open(PORTFILE, 'w') as file:
        file.write(port_before)
     
    print("Done.")
