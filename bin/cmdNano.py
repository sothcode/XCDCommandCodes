#! /usr/bin/python3

from talkNano import main

from moveNano import moveNano
from assignNano import assignNano
from homeNano import homeNano
from killNano import killNano
from reportNano import reportNano
from pulseNano import pulseNano
from configRevNano import configRevNano
from configNano import configNano

from commandDictionary import commDict

import sys


def cmdNano (argv):
    if (len(argv) > 0):
        command = argv[0]
        if command in commDict.keys():
            commDict[command](argv[1:])
        elif (command == "help"):
            print("Write as 'cmdNano.py [Command Name] [Any Arguments]\n")
            print("Valid commands are:")
            print(commDict.keys())
        else:
            print("Command not recognized- current valid commands are:")
            print(commDict.keys())
            return
    else:
        print("Command not recognized- current valid commands are:")
        print(commDict.keys())
        #print("Command not recongized- current valid commands are: move, assign, home, kill, report, pulse, configRev, config")
        return



if __name__ == "__main__":
    cmdNano(sys.argv[1:])
