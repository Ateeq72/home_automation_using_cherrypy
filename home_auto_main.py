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


class AteeqHomeAutomation:
    """ Sample request handler class. """
    @cherrypy.expose
    def index(self):
        my_ip = ([(s.connect(('8.8.8.8', 80)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1])
        return '''<!DOCTYPE html>
<html>
    <head>
        <meta charset="utf-8" />
        //<meta name="viewport" content="width=device-width, initial-scale=1, user-scalable=0;" />
        //<meta name="viewport" content="width=device-width"/>
        //<meta name="apple-mobile-web-app-capable" content="yes" />
        <title>
         Welcome To Ateeq's Home Automation
        </title>
        <link rel="stylesheet" href="static/jquery.mobile-1.0.1.min.css" />
        <script src="static/jquery.min.js">
        </script>
        <script src="static/jquery.mobile-1.0.1.min.js">
        </script>
        <script type="text/javascript">
        $(document).ready(function() {
            //stop the page from doing a stretch from the top when dragged ;
            //document.ontouchmove = function(event){ event.preventDefault(); };
            //move beyond the address  bar to hide ;
            //window.scrollTo(0, 1);
            //start button click code
            $("#auto").change(function () {$.post('/request',{key_pressed:"auto_"+$(this).val()})});
            $("#power1").change(function () {$.post('/request',{key_pressed:"power1_"+$(this).val()})});
            $("#power2").change(function () {$.post('/request',{key_pressed:"power2_"+$(this).val()})});
            $("#power3").change(function () {$.post('/request',{key_pressed:"power3_"+$(this).val()})});
            $("#stream").change(function () {$.post('/request',{key_pressed:"stream_"+$(this).val()})});
        });
        </script>
       </head>
    <body style="overflow: hidden;overflow-x:hidden;" onload="createImageLayer();">
        <div data-role="page" data-theme="a" id="page1">
            <div data-theme="a" data-role="header" data-position="">
                <h5>
                    Ateeq's <br> Home Automation
                </h5>
            </div>
            <div data-role="content">
                <div data-role="fieldcontain">
                    <fieldset data-role="controlgroup">
                        <label for="auto">
                        Automatic Mode! 
                        </label>
                        <select name="auto" id="auto" data-theme="a" data-role="slider">
                            <option value="off">
                                Off
                            </option>
                            <option value="on">
                                On
                            </option>
                        </select><br>
                       <label for="power1">
                       Switch One
                        </label>
                        <select name="power1" id="power1" data-theme="a" data-role="slider">
                            <option value="off">
                                Off
                            </option>
                            <option value="on">
                                On
                            </option>
                        </select><br>
                       <label for="power1">
                       Switch Two
                        </label>
                        <select name="power2" id="power2" data-theme="a" data-role="slider">
                            <option value="off">
                                Off
                            </option>
                            <option value="on">
                                On
                            </option>
                        </select><br>
                       <label for="power3">
                       Switch Three/ Switch Auto (Dont use if Auto!)
                        </label>
                        <select name="power3" id="power3" data-theme="a" data-role="slider">
                            <option value="off">
                                Off
                            </option>
                            <option value="on">
                                On
                            </option>
                        </select><br>
                       <label for="stream">
                       Use Me to toggle live<a href="http://%s:8091/stream_webcam.html"> webcam stream! </a> 
                        </label>
                        <select name="stream" id="stream" data-theme="a" data-role="slider">
                            <option value="off">
                                Off
                            </option>
                            <option value="on">
                                On
                            </option>
                        </select><br>
     <center>
            <form method="post" action="http://%s:8090/processform"> 
            Email: <input type="email" name="email"><br> 
            <input type="submit" value="Submit"> </form><br>
             <a href="/static/qrcode.html">QR-Code</a> to get connected to This WiFi!<br>
             Check Switches <a href="http://%s/status.html">history</a><br>
     </center>

                    </fieldset>
                </div>
            </div>
</div>
     </body>
</html>
''' % (my_ip,my_ip,my_ip)
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
            os.system("sudo service mjpg-streamer start")
        elif key == "stream_off":
            print "Stream Off!"
            os.system("sudo service mjpg-streamer stop")


        else:
            print key

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
        <meta charset="utf-8" />
    </head>
    <body>
    <center>
    <h1>Mail sent to %s </h1>
    </center>
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
