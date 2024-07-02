#! /usr/bin/python3

import os
import sys
import serial
import time
import math
from xcdSerial import sendline, getCurrentPort
from quickAssign import writeXCD2
from quickReport import readback, reportXCD2
from variableDictionaryXCD2 import varInterfaceAddresses as ADDR


# use input bytestring 
input_bytestring = ''


def velLatency(  ):



    return

def latencyTest():

    command = [228, 165, 0, 213, 8, 5, 6, 134, 1008, 0, 218]

    count = 7

    # reassign packet length and block length bytes
    command[4] = int(count+6)
    command[5] = int(count+3)
    # add stop byte
    command += [218]

    success,ret=sendline(getCurrentPort(),command)

    return success, ret


if __name__ == "__main__":
    if len(sys.argv) == 2:
        if sys.argv[1] == 'v':
            velLatency()
        else:
            latencyTest()
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


