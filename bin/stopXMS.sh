#! /bin/bash
#stty -F /dev/ttyUSB0 115200
for controller in `ls /dev/ttyUSB*`; do
    echo stopping $controller
    echo -e '\xE4\xA5\x00\xD5\x06\x03\x01\x0F\0xDA' > $controller
done
