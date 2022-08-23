#! /bin/bash
#stty -F /dev/ttyUSB3 115200
#echo -e '\xE4\xA5\xA4\x01\023' > /dev/ttyUSB3
od -x -N 1 < /dev/ttyUSB3

