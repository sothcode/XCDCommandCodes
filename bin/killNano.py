#! /usr/bin/python3

from talkNano import main

import sys

def killNano(argv):
    command_send = []
    command_code = "b1:23"
    command_send.append(command_code)
    main(command_send)

    print("killNano kills motion. Current motion is terminated, and the controller provides deceleration using KDEC parameter.")

    return

if __name__ == "__main__":
    killNano(sys.argv[1:])

