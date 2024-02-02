#! /bin/bash
#stty -F /dev/ttyUSB0 115200
# commnd below stops xms (\x03\x01\x0F), kills axis 0 (\x04\x05\x0A\x00)
# kills axis 1 (\x04\x05\x0A\x01), and disables both axes (\x04\x05\x08\xFF)
for controller in `ls /dev/ttyUSB*`; do
    echo stopping $controller
    echo  -e '\xE4\xA5\x00\xD5\x12\x03\x01\x0F\x04\x05\x0A\x00\x04\x05\x0A\x01\x04\x05\x08\xFF\xDA' > $controller
done
#must wait for them to actually be ready
sleep 3