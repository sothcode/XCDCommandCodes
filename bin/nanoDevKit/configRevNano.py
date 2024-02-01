#! /usr/bin/python3

from talkNano import main

import sys

def configRevNano(argv):
    command_send = []
    command_code = "b1:55"
    command_send.append(command_code)
    main (command_send)
    return


if __name__ == "__main__":
    configRevNano(sys.argv[1:])
