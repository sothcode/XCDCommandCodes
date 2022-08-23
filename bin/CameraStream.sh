#! /bin/bash
cd $LD_LIBRARY_PATH
echo "http://tpcpi.physics.sunysb.edu:8080/stream.html"
mjpg_streamer -o "output_http.so -w ./www" -i "input_raspicam.so" > /dev/null 2>&1 &
