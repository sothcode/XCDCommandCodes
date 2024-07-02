#! /bin/bash
#stty -F /dev/ttyUSB0 115200

start='date +%s%N'; 

end='date +%s%N'; 

echo $(( ($end - $start) ))