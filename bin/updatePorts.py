#! /usr/bin/python3

import glob


def getUARTPerPort():

    return



def find_ttyUSB_ports(folder='/dev'):
    # Use glob to find files matching the pattern /dev/ttyUSB*
    ttyUSB_ports = glob.glob(f'{folder}/ttyUSB*')

    # Return the list of found ttyUSB ports
    return ttyUSB_ports




if __name__ == "__main__":
    ttyUSB_ports = find_ttyUSB_ports()

    if ttyUSB_ports:
        print("Found ttyUSB ports:")
        for port in ttyUSB_ports:
            print(port)
    else:
        print("No ttyUSB ports found.")
