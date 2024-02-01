#! /usr/bin/python3

from readNano import readNano

import sys

def main(argv):
    #  This is the "e4 a5 a4" initial sequence...
    number = int(argv[0])
    print(number)

    b2 = number.to_bytes(2,'little')
    b2list = [str(b2[0]),str(b2[1])]
    print(b2list)

    b4 = number.to_bytes(4,'little')
    b4list = [str(b4[0]),str(b4[1]),str(b4[2]),str(b4[3])]
    print(b4list)

    return


if __name__ == "__main__":
   main(sys.argv[1:])
