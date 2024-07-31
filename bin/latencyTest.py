#! /usr/bin/python3

import os
import sys
import serial
import time
import math
from xcdSerial import sendline, getCurrentPort, _decode
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR


# use input bytestring 
input_bytestring = ''


def velLatency(  ):



    return

def latencyTest():

    # assign V0 = -1 so it 
    assignV0 = [228, 165, 0, 213, 8, 5, 6, 134, 1000, -1, 218]
    count = 8
    # reassign packet length and block length bytes
    assignV0[4] = int(count+6)
    assignV0[5] = int(count+3)

    # construct report V0 command until it reports back 0
    reportV0 = [228, 165, 0, 213, 8, 5, 6, 134, 1000, -1, 218]
    reportV0[4] = int(count+6)
    reportV0[5] = int(count+3)
    
    t1 = time.time()
    success,ret=sendline(getCurrentPort(),assignV0)
    
    while ret[0] != 0:
        success,ret=sendline(getCurrentPort(),reportV0)
    
    t2 = time.time()
    t = t2-t1

    return t, ret


def latencyLoop( numTimes=1 ):



    return



if __name__ == "__main__":
    if len(sys.argv) == 1:
        latencyLoop()
    elif len(sys.argv) == 2:
        try:
            n = float(sys.argv[1])
            latencyLoop(n)
        except ValueError:
            print("You didn't put in a number")
            sys.exit()
    else:
        print("STUPID")
        sys.exit()


# Example usage
# port = 'COM3'  # Replace with your serial port
# baudrate = 9600  # Replace with your baud rate
# input_bytestring = b'Hello, device!'  # Replace with your input bytestring

# latency, response = chatgpt_latency(port, baudrate, input_bytestring)
def chatgpt_latency(port, baudrate, input_bytestring):

    # Open the serial port
    with serial.Serial(port, baudrate, timeout=1) as ser:

        # Clear the input and output buffers
        ser.reset_input_buffer()
        ser.reset_output_buffer()

        # Record the start time
        start_time = time.time()

        # Send the bytestring to the device
        ser.write(input_bytestring)

        # Wait for the response
        response = ser.read(len(input_bytestring))  # Assuming the response length is same as input

        # Record the end time
        end_time = time.time()

        # Calculate the latency
        latency = end_time - start_time

        # Print or return the latency and response
        print(f"Response: {response}")
        print(f"Latency: {latency} seconds")

        return latency, response


