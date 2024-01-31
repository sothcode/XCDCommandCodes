#!/usr/bin/python3
import time
import serial
import sys
import struct

debug=False

def sendline(port, command):
    # the next portion of code is what establishes communication with the controller
    # and sends the bytestring command by serial comm
    #print("opening",port," with command string ", command)
    ser = serial
    try:
        ser = serial.Serial(
            port, #now drawn from input:  port='/dev/ttyUSB0', # Set serial port
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

    return False



def _readline(ser):
    #read the feedback from the serial port and return the response
    
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
    vals = _decode(resp)
    return vals


def _decode( resp ):
    #returns the array of floating point numbers that is packaged in resp (per nanomotion format)

    #resp structure is: (blocklength)(groupid)(reportid)(4bytes of float)(4bytes of float)... etc.
    #resp may contain multiple floating point numbers, all of which are little-endian.
    packlen=resp[0] #int.from_bytes(resp[0],byteorder='little')
    # print(packlen)
    nBytesExpected=packlen-3
    nBytes=len(resp)-3

    if (nBytes==1):
        #this means we are a single byte, so not a series of floats.
        return resp[3]

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




if __name__ == "__main__":
    debug=True
    int_array = [int(x) for x in sys.argv[2:]]
    sendline(sys.argv[1],int_array)
