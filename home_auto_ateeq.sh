#!/bin/sh
# chkconfig: 123456 90 10
# TTS Server for Speech Synthesis
#
workdir=/home/pi/HomeAutomation
 
start() {
    cd $workdir
    /usr/bin/python /home/pi/HomeAutomation/auto.py &
    echo "Server started."
}
 
stop() {
    pid=`ps -ef | grep '[p]ython /home/pi/HomeAutomation/auto.py' | awk '{ print $2 }'`
    echo $pid
    kill $pid
    sleep 2
    echo "Server killed."
}
 
case "$1" in
  start)
    start
    ;;
  stop)
    stop   
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo "Usage: /etc/init.d/home_auto_ateeq {start|stop|restart}"
    exit 1
esac
exit 0
