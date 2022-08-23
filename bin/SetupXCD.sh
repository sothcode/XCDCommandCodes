#! /bin/bash

# Set up the correct port speed for all four of the serial lines.
stty -F /dev/ttyUSB0 115200
stty -F /dev/ttyUSB1 115200
stty -F /dev/ttyUSB2 115200
stty -F /dev/ttyUSB3 115200
