#!/bin/bash
# 旋转小图标
incr=1
spin="/-\|"
echo -en "Please waiting...  \n"

while true
do
    printf "\b${spin:incr++%${#spin}:1}"
    sleep 0.1
done