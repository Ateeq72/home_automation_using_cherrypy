#!/usr/bin/python
# coding=utf-8
### ateeq72@xda 
import cherrypy
import RPi.GPIO as GPIO
import time
from time import sleep
import os
import sys
import socket
import subprocess
import mysql
import smtplib
import MySQLdb
import pymysql

from DBUtils.PersistentDB import PersistentDB

GPIO.setmode(GPIO.BOARD)

#set up the pins for relay

re1 = 7
re2 = 11
re3 = 13

#set'em up as required
	
GPIO.setup(re1,GPIO.OUT)
GPIO.setup(re2,GPIO.OUT)
GPIO.setup(re3,GPIO.OUT)

def connect(thread_index): 
        cherrypy.thread_data.db = MySQLdb.connect('localhost', 'ateeq', 'khader6@', 'usage_homeauto') 
    
cherrypy.engine.subscribe('start_thread', connect)

class AteeqHomeAutomation:

    @cherrypy.expose
    def index(self):
        my_ip = ([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
        return '''<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<title>jQuery Mobile: Theme Download</title>
	<link rel="stylesheet" href="static/ateeqsHA.min.css" />
	<link rel="stylesheet" href="static/jquery.mobile.icons.min.css" />
	<link rel="stylesheet" href="static/jquery.mobile.structure-1.4.5.min.css" />
	<script src="static/jquery-1.11.1.min.js"></script>
	<script src="static/jquery.mobile-1.4.5.min.js"></script>

<script type="text/javascript">
        $(document).ready(function() {
            $("#clear").click(function () {$.post('/request',{key_pressed:"empty"})});
            $("#flip-1").change(function () {$.post('/request',{key_pressed:"power1_"+$(this).val()})});
            $("#flip-2").change(function () {$.post('/request',{key_pressed:"power2_"+$(this).val()})});
            $("#flip-3").change(function () {$.post('/request',{key_pressed:"power3_"+$(this).val()})});
            $("#stream").change(function () {$.post('/request',{key_pressed:"stream_"+$(this).val()})});
            $("#auto").change(function () {$.post('/request',{key_pressed:"auto_"+$(this).val()})});
        });
</script>

</head>
<body>

	<div data-role="page" data-theme="a">
		<div data-role="header" data-position="inline">
			<h1>Ateeq's <br> Home Automation</h1>
		</div>
<center>
<div data-role="content" data-theme="a">
<div class="ui-field-contain">
        <label for="auto">Automatic Mode:</label>
        <select name="auto" id="auto" data-role="flipswitch">
            <option value="off">Off</option>
            <option value="on">On</option>
        </select>
    </div>
<div class="ui-field-contain">
        <label for="flip-1">Switch One:</label>
        <select name="flip-1" id="flip-1" data-role="flipswitch">
            <option value="off">Off</option>
            <option value="on">On</option>
        </select>
    </div>
<div class="ui-field-contain">
        <label for="flip-2">Switch Two:</label>
        <select name="flip-2" id="flip-2" data-role="flipswitch">
            <option value="off">Off</option>
            <option value="on">On</option>
        </select>
    </div>
<div class="ui-field-contain">
        <label for="flip-3">Switch Three:</label>
        <select name="flip-3" id="flip-3" data-role="flipswitch">
            <option value="off">Off</option>
            <option value="on">On</option>
        </select>
    </div>
<div class="ui-field-contain">
        <label for="stream">Stream Toggle:  <a href="http://%s:8091/stream_webcam.html"> local! </a> & <a href="http://ateeqhomeautomationstream.ngrok.com/stream_webcam.html">Worldwide Stream!</a></label>
        <select name="stream" id="stream" data-role="flipswitch">
            <option value="off">Off</option>
            <option value="on">On</option>
        </select>
    </div>
<div class="ui-field-contain">
<label for="clear">Check Switches <a href="http://%s/status.html">history</a></label>
<input type="button" id="clear" data-inline="true" value="Clear History">
</div>
<div class="ui-field-contain">
<a href="/qrcode">Click Here!</a> to get connected to this Wifi!
</div>
<div class="ui-field-contain">

<form method="post" action="processform"> 
<input type="email" name="email"  placeholder="Enter the E-Mail ID!"  value="">
<input type="submit" value="Submit"> 
</form>

</div>
</center>
</fieldset>
</div>
</div>
</body>
</html>
''' % (my_ip,my_ip)
    @cherrypy.expose
    def request(self, **data):
        # Then to access the data do the following
        #print data
        key = data['key_pressed'].lower()
        if key == "auto_on":
            print "Auto Mode On!"
            os.system("sudo service home_auto_ateeq.sh start")
            mysql.insertReading('auto_switch','on')
        elif key == "auto_off":
            print "Auto Mode Off!"
            os.system("sudo service home_auto_ateeq.sh stop")
            mysql.insertReading('auto_switch','off')
        elif key == "power1_on":
            print "p1 On"
            GPIO.output(re1, 1)    
            mysql.insertReading('switch_one','on')
        elif key == "power1_off":
            print "p1 Off"
            GPIO.output(re1, 0)
            mysql.insertReading('switch_one','off')
        elif key == "power2_on":
            print "p2 On"
            GPIO.output(re2, 1)
            mysql.insertReading('switch_two','on')
        elif key == "power2_off":
            print "p2 Off"
            GPIO.output(re2, 0)
            mysql.insertReading('switch_two','off')
        elif key == "power3_on":
            print "p3 On"
            GPIO.output(re3, 1)
            mysql.insertReading('switch_three','on')
        elif key == "power3_off":
            print "p3 Off"
            GPIO.output(re3, 0)
            mysql.insertReading('switch_three','off')
        elif key == "stream_on":
            print "Stream On!"
            subprocess.call("sudo service mjpg-streamer start", shell=True)
        elif key == "stream_off":
            print "Stream Off!"
            os.system("sudo service mjpg-streamer stop")
	elif key == "empty":
            print "Emptying Table!"
            mysql.removeEvery()
	  
        else:
            print key


    @cherrypy.expose
    def qrcode(self):
        return '''<!DOCTYPE html>
<html>
    <head>
    <meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="static/ateeqsHA.min.css" />
	<link rel="stylesheet" href="static/jquery.mobile.icons.min.css" />
	<link rel="stylesheet" href="static/jquery.mobile.structure-1.4.5.min.css" />
	<script src="static/jquery-1.11.1.min.js"></script>
	<script src="static/jquery.mobile-1.4.5.min.js"></script>
    </head>
    <body>
        <div data-role="page" data-theme="a">
            <div data-role="header" data-position="inline">
                <h1>
                    Ateeq's <br> Home Automation
                </h1>
            </div>
    <center>
    <img src="/static/wifi.png" /><br>
    Scan this code with your Smart Phone usind Qr-Code scanner!
    </center>
    </div>
    </body>
</html>'''
        

    @cherrypy.expose
    def processform(self, email):
        smtpserver = 'smtp.gmail.com:587'
        authreq = 1
        smtpuser='ahmedateeq64@gmail.com'
        smtppass='<secret>'
        FROM = 'ahmedateeq64@gmail.com'
        TO = [email]
        SUBJECT = "Hi Greetings from Ateeq."
        TEXT = "Click on this Address to control devices http://ateeqhomeautomation.ngrok.com"
        # Prepare actual message
        message = """\From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        sender = 'ahmedateeq64@gmail.com'
        session = smtplib.SMTP(smtpserver)
        session.ehlo()
        session.starttls() 
        if authreq:
           session.login(smtpuser,smtppass)
           smtpresult = session.sendmail(sender,email,message)
        if smtpresult: 
           errstr = "" 
           for recip in smtpresult.keys(): 
               errstr = """Could not delivery mail to: %s Server said: %s 
                           %s 
                           %s""" % (email, smtpresult[email][0], smtpresult[email][1], errstr) 
           raise smtplib.SMTPException, errstr 
        return '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">
	<link rel="stylesheet" href="static/ateeqsHA.min.css" />
	<link rel="stylesheet" href="static/jquery.mobile.icons.min.css" />
	<link rel="stylesheet" href="static/jquery.mobile.structure-1.4.5.min.css" />
	<script src="static/jquery-1.11.1.min.js"></script>
	<script src="static/jquery.mobile-1.4.5.min.js"></script>
    </head>
    <body>
       <div data-role="page" data-theme="a">
		<div data-role="header" data-position="inline">
               <h1>
                    Ateeq's <br> Home Automation
                </h1>

            </div>
    <center>
    <h1>Mail sent to %s </h1>
    </center>
    </div>
    </body>
</html>''' % (email)

        
import os.path
tutconf = os.path.join(os.path.dirname(__file__), 'config.conf')

if __name__ == '__main__':
    # CherryPy always starts with app.root when trying to map request URIs
    # to objects, so we need to mount a request handler root. A request
    # to '/' will be mapped to HelloWorld().index().
    cherrypy.quickstart(AteeqHomeAutomation(), config=tutconf)
else:
    # This branch is for the test suite; you can ignore it.
    cherrypy.tree.mount(AteeqHomeAutomation(), config=tutconf)
