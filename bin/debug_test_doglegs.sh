#!/bin/bash

# Iterate over all serial controllers we find matching /dev/ttyUSB*
for ser in /dev/ttyUSB*; do
    # Check if the file exists
    if [ -e "$ser" ]; then
        # Run the command
	echo "$ser" > XCD_current_port
	echo "AXIS 0:"
        ./quickAssign FPOS 0
	./quickAssign XAXIS 0
	./gotoDogleg 2.9
	./gotoDogleg -2.9
	./gotoDogleg 0
	echo "AXIS 1:"
       ./quickAssign FPOS 0
	./quickAssign XAXIS 1
	./gotoDogleg 2.9
	./gotoDogleg -2.9
	./gotoDogleg 0
    else
        echo "port not found by shell.  Huh?"
    fi
done
