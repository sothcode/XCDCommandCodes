#! /usr/bin/python3

from readXCD2 import readXCD2

#test

import sys
import struct

#talkNano assembles the command to the XCD chip in bytes.

def main(argv):
    #  This is the "e4 a5 a4" initial sequence...
    command = [ '228', '165', '0', '213', '0']
    count = 0
#    print(argv)
#    print(type(argv))
    for item in argv:
# Defines the types of command parameters:
# b1: integer of 1 byte
# i2: integer of 2 bytes
# i4: integer of 4 bytes
# u2: unsigned integer of 2 bytes
# r4: real number of 4 bytes
#        print(item)
#        print(type(item))
        format = item[0:2]
#        print(format)
        if (format == "b1"):
            number = int(item[3:])
            b1 = number.to_bytes(1,byteorder='little',signed=True)
            b1list = [str(b1[0])]
            command += b1list
            count += 1
        elif (format == "i2"):
            number = int(item[3:])
            b2 = number.to_bytes(2,byteorder='little',signed=True)
            b2list = [str(b2[0]),str(b2[1])]
            command += b2list
            count += 2
        elif (format == "i4"):
            number = int(item[3:])
            b4 = number.to_bytes(4,byteorder='little',signed=True)
            b4list = [str(b4[0]),str(b4[1]),str(b4[2]),str(b4[3])]
            command += b4list
            count += 4
        elif (format == "u2"):
            number = int(item[3:])
            u2 = number.to_bytes(2,byteorder='little',signed=False)
            u2list = [str(u2[0]),str(u2[1])]
            command += u2list
            count += 2
        elif (format == "r4"):
            number, = struct.unpack('!I', struct.pack('!f', float(item[3:])))
            r4 = number.to_bytes(4,byteorder='little',signed=False)
            r4list = [str(r4[0]),str(r4[1]),str(r4[2]),str(r4[3])]
            command += r4list
            count += 4
        else:
            print(item)
            print("Known formats are b1 i2 i4 u2 and r4")
            return
    command[3] = str(count)
#    print(command)
    e = readNano(command)
# After assembling the command structure with prefix, commands and arguments, send into readNano to send command to chip
#    print(e)
    return


if __name__ == "__main__":
   main(sys.argv[1:])
