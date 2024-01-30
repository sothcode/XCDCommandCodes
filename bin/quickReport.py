#!/usr/bin/python3
import time
import serial
from variableDictionaryXCD2 import varDict
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
import sys
import struct

debug=False


def decodeRead( resp ):
    #resp structure is: (blocklength)(groupid)(reportid)(4bytes of float)(4bytes of float)... etc.
    #resp may contain multiple floating point numbers, all of which are little-endian.
    packlen=resp[0] #int.from_bytes(resp[0],byteorder='little')
    # print(packlen)
    nBytesExpected=packlen-3
    nBytes=len(resp)-3

    if (nBytesExpected!=nBytes):
        print("expected payload of ", nBytesExpected, " bytes but resp contains ", nBytes, " bytes.  Failing.")
        return 0

    if(nBytes %4 !=0): #same as '&3 != 0'
        print("payload has ", nBytes, "bytes, which is not a whole number of floats.  Failing.")
        return 0

    nFloats=int(nBytes/4)
    decode=[0]*nFloats
    for i in range(0,nFloats):
        decode[i]=struct.unpack_from('<f', resp, i*4+3)[0]
    return decode

def readback(arg):
    #readback the value at one address.
    check,ret = reportXCD2([arg])
    if check==False:
        print("CRITICAL FAILURE. Communication error.")
        sys.exit()
    if debug:
        print("_readback result: ", ret[0])
    return ret[0]

def _readline(ser):
    # read and interpret the reply's "header" and name it in bytes (5 bytes)
    e4 = ser.read(1) # Prefix - UART sync byte 1 (constant x\E4)
    a5 = ser.read(1) # Prefix - UART sync byte 2 (constant x\A5)
    a4 = ser.read(1) # Prefix - Destination Address (\x00 for XCD2 UART protocol)
    d5 = ser.read(1) # Prefix - Start index
    NN = ser.read(1) # Prefix - Packet length in bytes (includes start index, not sync bytes or address)
    NN = int.from_bytes(NN, "big")
    #'NN' includes two bytes we don't need:  1 is the byte which contains NN itself, which we have already read.  the other is the byte at the very end, which we do not need to read.  Hence we need nBytes:
    nPayloadBytes=NN-3

    # read the requested number of bytes as stipulated in the header to read commands and arguments
    line = bytearray([]) #[NN]) #an array whose first element is NN
    for i in range(0,nPayloadBytes): #this is inclusive, so skips NN-1, which is the stop index.
        c = ser.read(1)
        if c:
            # print(c)
            line += c
        else:
            break
    # resp = e4 + a5 + a4 + d5 + bytes(line)
    resp = line #bytes(line)
    hex_values = ' '.join(hex(byte) for byte in line)
    #print("_readline old:",resp)
    if debug:
        print("_readline:",hex_values)
    vals = decodeRead(resp)
    return vals


def reportXCD2( argv ):
    if argv:
        if len(argv) > 10:
            print("Too many variables trying to be assigned.  Max 10 variables can be assigned at once.")
            return False, 0

        var_names = argv
        if debug:
            print(var_names)
        
        getAxis = reportXCD2noAxis([varDict['XAXIS']])

        ax_int = int(getAxis)
        ax_byte = ax_int.to_bytes(1,byteorder='little',signed=True)
        ax_comm = [int(ax_byte[0])]
        
        command = [228, 165, 0, 213, 0, 0, 6, 132]
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
                return False, 0
            
            command += ax_comm
            count += 1

    else:
        print("No arguments given. reportXCD2 parameters are: \n \
               1) Variable- Mandatory, variable to report value of. For full list of variables, refer to variableDictionary. \n \
               2-10) Variable - Optional, other variables to report. \
               ")
        return False, 0

    # reassign packet length and block length bytes
    command[4] = int(count+6)
    command[5] = int(count+3)
    # add stop byte
    command += [218]
    if debug:
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
            #response = '{}'.format(_readline(ser))
            response=_readline(ser)
            ser.close()
            if debug:
                print(response)
            return True, response
        print("Serial port not open - check to see that usb is properly connected, or motor is powered.")
        return False, 0

    except serial.serialutil.SerialException:
        print("Serial Exception- check to see that usb is properly connected, or motor is powered.")
        return False, 0

    return False, 0



def reportXCD2noAxis( argv ):
    if argv:
        if len(argv) > 10:
            print("Too many variables trying to be assigned.  Max 10 variables can be assigned at once.")
            return False, 0

        var_names = argv
        if debug:
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
                return False, 0

    else:
        print("No arguments given. reportXCD2 parameters are: \n \
               1) Variable- Mandatory, variable to report value of. For full list of variables, refer to variableDictionary. \n \
               2-10) Variable - Optional, other variables to report. \
               ")
        return False, 0

    # reassign packet length and block length bytes
    command[4] = int(count+6)
    command[5] = int(count+3)
    # add stop byte
    command += [218]
    if debug:
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
            #response = '{}'.format(_readline(ser))
            response=_readline(ser)
            ser.close()
            if debug:
                print(response)
            return True, response
        print("Serial port not open - check to see that usb is properly connected, or motor is powered.")
        return False, 0

    except serial.serialutil.SerialException:
        print("Serial Exception- check to see that usb is properly connected, or motor is powered.")
        return False, 0

    return False, 0


if __name__ == "__main__":
    debug=True
    reportXCD2(sys.argv[1:])
