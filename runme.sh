#!/bin/bash
cd /home/pi/HomeAutomation/

sudo python home_auto_main.py &
sleep 2
screen -d -m ./ngrok -subdomain "ateeqhomeautomation" 8090


 
