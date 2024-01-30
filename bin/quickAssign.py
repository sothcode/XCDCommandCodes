#!/usr/bin/python3
import time
import serial
from variableDictionaryXCD2 import varDict
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from variableDictionaryXCD2 import varStatusValues as STAT
from quickReport import readback, reportXCD2noAxis
import sys
import struct

debug=False
sleeptime=0.1

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
            line += c
        else:
            break
        resp = e4 + a5 + a4 + d5 + bytes(line)
    return resp


def sendcommand(com,arg):
    if debug:
        print("command:  Check status:")
    status=readback(ADDR['STATUS'])
    if status!=STAT['READY']:
        print("NOT EXECUTED.  Error: Controller is not in ready state.  Status=",status)
        sys.exit()
    try:
        input = float(arg)
    except ValueError:
        print("NOT EXECUTED.  Error: Not a valid number, arg=",arg)
        sys.exit()

    if debug:
        print("command: set argument:")    
    writeXCD2([ADDR['ARG'], arg])    
    if debug:
        print("command: set status to new_command:")    
    writeXCD2([ADDR['STATUS'], STAT['NEWCOMMAND']])
    #set the command byte last, so we know we don't have a race condition
    if debug:
        print("command: set command byte:")    
    writeXCD2([ADDR['COMMAND'],com])

    #now wait until the status changes to indicate the command has been acted on:
    if debug:
        print ("command: priming status check before wait")
    status=readback(ADDR['STATUS'])
    print("command says status is ",status)
    while status==STAT['NEWCOMMAND']:
        if debug:
            print ("command: waiting for device to ack command:")
        status=readback(ADDR['STATUS'])
        time.sleep(sleeptime)

    return
    

def writeXCD2( argv ):
    if argv:
        if len(argv) > 14:
            print("Too many variables trying to be assigned.  Max 7 variables can be assigned at once.")
            return

        var_names = argv[::2]
        real_vals = argv[1::2]
        if debug:
            print(var_names, real_vals)
        # if len(var_names) != len(real_vals):
        #    print("Formatting error: likely missing/extra variable or value to be assigned. Please check input.")
        #    return

        getAxis = reportXCD2noAxis([varDict['XAXIS']])

        ax_int = int(getAxis)
        ax_byte = ax_int.to_bytes(1,byteorder='little',signed=True)
        ax_comm = [int(ax_byte[0])]


        command = [228, 165, 0, 213, 0, 0, 6, 134]
        count = 0
        for i in range(0, len(var_names)):
            var = var_names[i]
            val = real_vals[i]

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

            try:
                float(val)
            except ValueError:
                print("Value to assign - " + val + " - must be a real number.")
                return
            else:
                number, = struct.unpack('!I', struct.pack('!f', float(val)))
                r4 = number.to_bytes(4,byteorder='little',signed=False)
                val_command = [int(r4[0]), int(r4[1]), int(r4[2]), int(r4[3])]
                command += val_command
                count += 4

            command += ax_comm
            count += 1
            

            

    else:
        print("No arguments given. writeXCD2 parameters are: \n \
               1) Variable- Mandatory, determines the variable to change the value of. Refer to variableDictionary for a full list of variables. \n \
               2) Value - Mandatory, determines value to change variable to. Real value.  \n ")
        return

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
            return response
        return "9999999"

    except serial.serialutil.SerialException:
        return "Serial Exception- check to see that usb is properly connected, or motor is powered."

    return


if __name__ == "__main__":
    debug=True
    writeXCD2(sys.argv[1:])
