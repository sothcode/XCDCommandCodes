#! /usr/bin/python3

import os
import sys
import re
import time
import random
from changeAxisDogleg import changeAxis
from quickReport import readback, reportXCD2
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR
from homePhi import homePhi
from goto import find_comm_and_set_tuning, goto

# set reset command - just run shell script
stopXMS = './killXCD2.sh'
startXMS = './startXMS.sh'
reset = './debug_reset_doglegs.sh'

# Initialize file to store movement report
REPORTFILE = ''

# SET GLOBAL VARIABLES
lb = 0.0        # low bound to travel to
hb = 0.0        # high bound to travel to
t_hang = 0.3    # wait time between successive gotoDogleg calls




def clean_filename(input_string):
    # Remove any characters that are not valid in filenames
    return re.sub(r'[<>:"/\\|?*]', '_', input_string)



# for given axis, first home - doesn't do this yet
# record bounds, then choose a random point within bounds
# record past position
# openloop to new random point and record the arrived position
# repeat as many times as necessary
def testOLAccuracy( axis, numPoints=1 ):

    # check numPoints greater than 0
    if numPoints <= 0:
        print("OLAccuracyTest.py needs a nonzero number of times to move.")
        return

    # check status, then initialize proper variables
    status=readback(ADDR['STATUS'])
    if status!=0:
        print("OLAccuracyTest.py initilization failed. Please check status.")
        return

    # change to input axis (and check if axis exists)
    s = changeAxis(axis)
    if not s:
        print("OLAccuracyTest.py: did not change axis properly.")
        return False

    # set command lookup table to match the axis
    # isDogleg,COMM=find_comm_and_set_tuning(axis)


    # Create file from input axis after cleaning name just in case
    filename = clean_filename(axis)
    REPORTFILE = filename + "_OLtest.txt"

    # update low bound and high bound according to input axis
    lb = float(readback(ADDR['HARD_STOP1']))
    hb = float(readback(ADDR['HARD_STOP2']))

    # loop through as many times as specified
    for i in range(numPoints):

        old_pos = readback(ADDR['FPOS'])

        # choose a random point in between bounds
        destination = random.uniform(lb, hb)

        # record start time of open-loop move
        t1 = time.time()

        # move to random point using open-loop
        didGoTo, position = goto(axis, destination, True)
        if not didGoTo:
            print("OLAccuracyTest.py: goto move iteration ", i, " failed.")
            return

        #record end time of open-loop move
        t2 = time.time()

        # write to file previous location, new desired location, new arrived location, and move time
        with open(REPORTFILE, "a") as file:
            file.write('%s %s %s %s\n' % (old_pos, destination, position, t2-t1))

        # sleep a little before next iteration
        time.sleep(t_hang)
            
    # when done with loop
    # print("OLAccuracyTest.py REPORT: startTime = ", tRunStart,
    #         "\n AXIS 0:", "\n\t home ({:.5g}) --> hb ({:.5g}): ".format(home, posi[0]), t_arr[1]-t_arr[0])

    return



if __name__ == "__main__":
    #check args
    if len(sys.argv) == 2:
        axis = sys.argv[1]
        testOLAccuracy(axis)
    elif len(sys.argv) == 3:
        axis = sys.argv[1]
        numTimes=sys.argv[2]
        try:
            numPts = int(numTimes)
        except ValueError:
            print("NOT EXECUTED. Second argument can only be an integer to denote number of times to loop.  Correct usage is:")
            print("   ./OLAccuracyTest.py laser_name loop_number(int)")
            sys.exit()
        testOLAccuracy(numPts)
    else:
        print("NOT EXECUTED. Wrong number of arguments.  Correct usage is:")
        print("   ./OLAccuracyTest.py laser_name loop_number")
        sys.exit()