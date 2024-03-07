#! /usr/bin/python3

import os
import sys
import time
import math
from quickReport import readback, reportXCD2
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR

# to load tty data from the db so we know which tty we want:
sys.path.append("kfDatabase")
import kfDatabase

# tuning settings
sleeptime=0.5 #in seconds
debug=False
mainDb = 'test_only_axis_parameters.kfdb'


def setLight( attenuator=None, inputval=None ):

    if attenuator==None or inputval==None:
        print("wrong args for goto.  requires two arguments.")
        return False

    #check if controller is busy.  If so, exit with explanation
    if debug:
        print("goto:  Check status:")
    status=readback(ADDR['STATUS'])

    # check status
    if status!=0:
        print("NOT EXECUTED. Controller status is not 0.")
        return False, 0
    # convert attenuator percentage from str to float
    try:
        percentage = float(inputval)
    except ValueError:
        print("Error: Not a valid number")
        return False, 0
    
    # find minlight and maxlight positions from database
    minKey = attenuator+"/minlight"
    maxKey = attenuator+"/maxlight"
    # get the value from the dict.
    if debug:
        print("goto: looking for attenuator min/max values %s/%s"% (minKey, maxKey))
    minPos = -1000
    maxPos = -1000
    maxBool,maxPos=kfDatabase.readVar(mainDb, maxKey)
    minBool,minPos=kfDatabase.readVar(mainDb, minKey)
    # check that it returned successfully
    if not (minBool or maxBool):
        print("goto: kfDatabase failed.  minLight '%s' or maxLight '%s' (or both) not found. (kfdb=%s, , minKey=%s, maxKey=%s)" % (minPos,maxPos,mainDb,minKey,maxKey))
        return False        
    #  check to see if the dict value is a number.
    #  if number: make it a float.
    if (is_number(minPos)):
        targetPos=float(minPos ) 
    else:
        print("goto: kfDatabase key '%s' has non-numeric value %s" % (maxKey,str(minPos)))
        return False



    # we presume the attenuator has a sin^2() profile
    desired_pos = 4/math.pi*(math.asin(math.sqrt(percentage)))

    return



if __name__ == "__main__":
    #check args
    if len(sys.argv)==3:
        #keep current leg, assume arg is destination.
        attenuator=sys.argv[1]
        inputval = sys.argv[2]
        setLight( attenuator, inputval )
    else:
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is:")
        print("     ./setLight.py ATT# [position]")
        sys.exit()
    #if wrong arguments, exit with explanation