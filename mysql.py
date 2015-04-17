#-------------------------------------------------------------------------------
# Name:        MySQL reader/writer
# Purpose:
#
# Author:      Jakub 'Yim' Dvorak
#
# Created:     26.10.2013
# Copyright:   (c) Jakub Dvorak 2013
# Licence:
#   ----------------------------------------------------------------------------
#   "THE BEER-WARE LICENSE" (Revision 42):
#   Jakub Dvorak wrote this file. As long as you retain this notice you
#   can do whatever you want with this stuff. If we meet some day, and you think
#   this stuff is worth it, you can buy me a beer in return.
#   ----------------------------------------------------------------------------
#-------------------------------------------------------------------------------
import MySQLdb

from time import strftime,localtime
import datetime
from unidecode import unidecode

def connect():
    # Mysql connection setup. Insert your values here
    return MySQLdb.connect(host="localhost", user="ateeq", passwd="khader6@", db="usage_homeauto")

def insertReading(switch,action):
    db = connect()
    cur = db.cursor()
    currentTime=strftime("%Y%m%d%H%M%S", localtime())
    cur.execute("""INSERT INTO usage_made (switch, action, time) VALUES (%s, %s, %s)""",(switch,action,currentTime))
    db.commit()
    db.close()
    print "Done Inserting"
