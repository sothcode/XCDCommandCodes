#! /usr/bin/python3

from updatePorts import find_ttyUSB_ports

def displayPorts():
    ttyUSB_ports = find_ttyUSB_ports()

    if not ttyUSB_ports:
        print("No ttyUSB ports found.")
    else:
        print("Found ttyUSB ports:")
        for port in ttyUSB_ports:
            print(port)

    return


if __name__ == "__main__":
    displayPorts()
