#! /usr/bin/python3

import sys
import glob
from variableDictionaryXCD2 import varUniqueID as AXID
from quickReport import reportXCD2noAxisPort

filename = './xcd2_ports.kfdb'


def updatePorts():

    # create lookup table of axis variables to compare UART addresses to
    IDlookup = {v:k for k, v in AXID.items()}

    # find open ports
    ttyUSB_ports = find_ttyUSB_ports()

    with open(filename, "w") as file:

        # then for each port find UART addresses and reverse lookup motor IDs
        for port in ttyUSB_ports:

            # now get
            UART0, UART1 = getUART01_Address(port)

            
        
            # Logs the change to the log for a change
            file.write('%s %s\n' % ('UART0', UART0))
            file.write('%s %s\n' % ('UART1', UART1))

    return


def getUART01_Address( port ):

    if port is None:
        ttyUSB_ports = find_ttyUSB_ports()
        print("Need to specify which port to access variables from.  Possible ports are ", ttyUSB_ports)
        sys.exit()
    
    getBool, UART = reportXCD2noAxisPort(port, ['UART0_ADDRESS', 'UART1_ADDRESS'])

    if getBool==False:
        print("CRITICAL FAILURE. Communication error. ttyUSB found but not corresponding to valide motor axis.")
        sys.exit()

    UART0 = int(UART[0])
    UART1 = int(UART[1])
    
    return UART0, UART1



def find_ttyUSB_ports():
    # Use glob to find files matching the pattern /dev/ttyUSB*
    ttyUSB_ports = glob.glob('/dev/ttyUSB*')

    # Return the list of found ttyUSB ports
    return ttyUSB_ports


if __name__ == "__main__":
    updatePorts()
