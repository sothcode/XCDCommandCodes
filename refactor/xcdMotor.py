#! /usr/bin/python3
#
#  xcdMotor.py
#
#  Created by Seth Howell on 2/3/24.
#  Copyright © 2024. All rights reserved.

import os
import sys
import re

sys.path.append("../bin/")
import variableDictionaryXCD2
from variableDictionaryXCD2 import varAllCommands as ALL_COMM
from variableDictionaryXCD2 import varStatusValues as STAT
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR



# startup idea:
# updatePorts whenever plugging something in or unplugging it (including power cycles).
#    that creates a file with lines arranged:  laser portname axis
# homeEggs
# homePhi for all phis we find
# homeThetaS for all thetaS
# homeThetaL for all thetaL


# Controller has:
# Motor x2
# currentAxis
# port
# something to check whether a port is in use (ttyUSB0.lock)
class Controller:

    def __init__():
        return

    def getPort():
        currentPort="NO_PORT"
        with open(PORTFILE, 'r') as file:
            currentPort = file.readline().rstrip()
        return currentPort
    
    def getMotors():
        return



# Motor class
# port
# name
# typeOfMotor
# axis
# access to kfdb to read positions or other properties we store
# writing to kfdb must be done serially, so maybe it prints write requests
# in full lines to the screen for humans to copy/paste?
class Motor:

    def __init__(self, name):
        # look up if name exists in database file
        # if so assigns name and finds other 

        self.name = name
# function:
#    constructor(name)
#       look up the correct port and axis
#       look for a lockfile on that axis
#       set a lockfile, or return None
#    return the motor 


        self.type = self.getMType()
        self.axis = self.getAxis()
        self.port = self.getPort()

        return
    
    def isName():



        return True

    def getMType(axisName):
        #return a command lookup table matching the axis.
        #also let us know if the axis is a dogleg, so we know how to behave.
        isDogleg=False
        COMM={}
        if bool(re.match(r'^.+_DL\d_A\d$',axisName)):
            COMM=ALL_COMM['Dogleg']
            isDogleg=True
        elif bool(re.match(r'^.+_TH_S$',axisName)):
            COMM=ALL_COMM['ThetaS']
        elif bool(re.match(r'^.+_TH_L$',axisName)):
            COMM=ALL_COMM['ThetaL']
        elif bool(re.match(r'^.+_PH$',axisName)):
            COMM=ALL_COMM['Attenuator']        
        elif bool(re.match(r'^.+_PH$',axisName)):
            COMM=ALL_COMM['Attenuator']
        else:
            print("no match of '%s' to axis types.  Critical failure!"%(axisName))
            sys.exit()
        return isDogleg, COMM

    def getAxis():
        return 
    
    def getPort():
        return 
    
    def home():
        #    go to all the .s19-findable positions: (hard stops, home tick)
        #    check those against the db
        #    if all is well, return true.
        #    if all is not well, update db, print caution to screen with new data.
        return
    
    def gotoStr( str ):
        #    looks up the string in the Db, goes there, returns true if it made it
        return True

    def gotoFloat( val ):
        #    goes to that point, returns true if it made it.
        return True

    def getVar(variable):

        return
        
    def setVar(variable, value):

        return
    
    def __del__(self):
        #    removes the lock file
        #    destroys instance of motor
        return

