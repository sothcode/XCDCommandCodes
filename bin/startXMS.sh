#! /bin/bash
#stty -F /dev/ttyUSB0 115200
for controller in `ls /dev/ttyUSB*`; do
    echo starting $controller
    echo -e '\xE4\xA5\x00\xD5\x06\x03\x01\x0E\0xDA' > $controller
done
