#! /usr/bin/python3

from talkNano import main

import sys

def ping(argv):
    command_send = []
    group_number = "u1:0"
    command_code = "u1:5"

    command_send.append(group_number)
    command_send.append(command_code)

    if argv:
        for item in argv:
            parameter = str(item)
            param_code = "u1" + parameter
            command_send.append(param_code)
        if len(command_send) > 21:
            print("Maximum size is 20 bytes. Please repeat with fewer parameters.")
            return

    print("pingNano is a basic communication test command. It will copy the payload sent, if it exists, to the reply packet.")
    #main (command_send)
    return


if __name__ == "__main__":
    ping(sys.argv[1:])
