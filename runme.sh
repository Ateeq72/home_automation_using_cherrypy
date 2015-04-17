#!/bin/bash
cd /home/pi/HomeAutomation/

sudo python home_auto_main.py &
sleep 2
./ngrok -subdomain "ateeqhomeautomation" 8090 &


 
