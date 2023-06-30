#!/usr/bin/python3
import time
import serial
from variableDictionaryXCD2 import varDict
import sys
import struct


def decodeRead():
    return


def _readline(ser):
    # read and interpret the reply's "header" and name it in bytes (5 bytes)
    e4 = ser.read(1) # Prefix - UART sync byte 1 (constant x\E4)
    a5 = ser.read(1) # Prefix - UART sync byte 2 (constant x\A5)
    a4 = ser.read(1) # Prefix - Destination Address (\x00 for XCD2 UART protocol)
    d5 = ser.read(1) # Prefix - Start index
    NN = ser.read(1) # Prefix - Packet length in bytes (includes start index, not sync bytes or address)
    NN = int.from_bytes(NN, "big")

    # read the requested number of bytes as stipulated in the header to read commands and arguments
    line = bytearray([NN])
    for i in range(0,NN-2):
        c = ser.read(1)
        if c:
            print(c)
            line += c
        else:
            break
        resp = e4 + a5 + a4 + d5 + bytes(line)
    return resp


def reportXCD2( argv ):
    if argv:
        if len(argv) > 10:
            print("Too many variables trying to be assigned.  Max 10 variables can be assigned at once.")
            return

        var_names = argv
        print(var_names)

        command = [228, 165, 0, 213, 0, 0, 6, 4]
        count = 0
        for i in range(0, len(var_names)):
            var = var_names[i]

            if var in varDict.keys():
                var_num = varDict[var]
                u2 = var_num.to_bytes(2,byteorder='little',signed=False)
                var_command = [int(u2[0]), int(u2[1])]
                command += var_command
                count += 2
            else:
                print("Variable name - " + var + " -  not recognized. Variable list given as:")
                print(varDict.keys())
                return

    else:
        print("No arguments given. reportXCD2 parameters are: \n \
               1) Variable- Mandatory, variable to report value of. For full list of variables, refer to variableDictionary. \n \
               2-10) Variable - Optional, other variables to report. \
               ")
        return

    # reassign packet length and block length bytes
    command[4] = int(count+6)
    command[5] = int(count+3)
    # add stop byte
    command += [218]
    print(command)

    # the next portion of code is what establishes communication with the controller
    # and sends the bytestring command by serial comm
    ser = serial
    try:
        ser = serial.Serial(
            port='/dev/ttyUSB0', # Set serial port
            baudrate=115200,     # Set baud rate
            parity=serial.PARITY_NONE,
            bytesize=serial.EIGHTBITS
        )
        if (ser.isOpen()):
            phrase = bytes(command)
            ser.write(phrase)
            response = '{}'.format(_readline(ser))
            ser.close()
            print(response)
            return response
        return "9999999"

    except serial.serialutil.SerialException:
        return "Serial Exception- check to see that usb is properly connected, or motor is powered."

    return


if __name__ == "__main__":
   reportXCD2(sys.argv[1:])


