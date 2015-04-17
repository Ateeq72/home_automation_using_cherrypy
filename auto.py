import RPi.GPIO as GPIO
import time
from time import sleep

ir = 15
re3 = 13

GPIO.setmode(GPIO.BOARD)

GPIO.setup(ir, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(re3,GPIO.OUT)
while True:
  try:
     if GPIO.input(ir) == 1:
       GPIO.output(re3,1)
       sleep(5)
       print "Relay On!"
     elif GPIO.input(ir)  == 0:
       GPIO.output(re3,0)
       print "Relay Off"
  except KeyboardInterrupt:
     GPIO.cleanup()

