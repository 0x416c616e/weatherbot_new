#!/usr/bin/env bash
#intended to run on a raspberry pi zero w
#requires that the zero w is running as an SFTP server
#also has a dependency of libimage-exiftool-perl

while :
do
    raspistill -o sky.jpg -rot 270 -roi 0.15,0.5,0.3,0.3
    exiftool -all= sky.jpg
    echo -n "Took new photo at "
    date
    sleep 600 #10 minutes
done
