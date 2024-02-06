#! /bin/bash
#stty -F /dev/ttyUSB0 115200
echo -e '\xE4\xA5\x00\xD5\x06\x03\x06\x0E\0xDA' > /dev/ttyUSB0
