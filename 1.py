import MySQLdb as mdb
import grovepi
import time
mq5sensor = 0           #connect to A0
grovepi.pinMode(mq5sensor,"INPUT")
moisture_sensor = 1         #connect to A1
grovepi.pinMode(moisture_sensor,"INPUT")
interval = 3
while True:
    try:
        val = (grovepi.analogRead(mq5sensor)/102.4)
        mq5 = str(val/10)
    except(IOError):
        mq5 = "NAN"
    print("MQ5 at Node *: " + mq5)
    try:
        val = grovepi.analogRead(moisture_sensor)
        moi = str(val)
    except(IOError):
        moi = "NAN"
    print("Moisture content at Node *: " + moi)
    time.sleep(interval)


    
