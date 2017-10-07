###3 gas sensors connected at A0,A1
import MySQLdb as mdb
import grovepi
import time
#import RPi.GPIO as gpio
#gpio.setmode(gpio.BOARD)
#gpio.setwarnings(False)
mq5sensor = 0           #connect to A2
grovepi.pinMode(mq5sensor,"INPUT")
#gpio.setup(18,gpio.IN)
mq2_1sensor = 1         #connect to A1
grovepi.pinMode(mq2_1sensor,"INPUT")
#mq2_2sensor = 2
#grovepi.pinMode(mq2_2sensor,"INPUT")
#count = 0
threshold = 10         #replace this value by the threshold value
#msg1 = 'positive'
#msg2 = 'negitive'
tim = 2                 #time to delay
con=mdb.connect('localhost','user','1234','gas_read');
with con:
    cur = con.cursor()
    #cur1 = con.cursor()
    #cur2 = con.cursor()
    #cur3 = con.cursor()
    #cur.execute("drop table if exists <table name>")
    cur.execute("create table if not exists node1(Time datetime,MQ5 varchar(9))")
    cur.execute("create table if not exists node2(Time datetime,MQ2 varchar(9))")
    cur.execute("create table if not exists node3(Time datetime,MQ2 varchar(9))")
    cur.execute("create table if not exists Readings(Time datetime,Node1 varchar(9),Node2 varchar(9),Node3 varchar(9))")
while True:
    alert = 0           #resets every time
    try:
        temp = (grovepi.analogRead(mq5sensor)/102.4) #divide by 102.4 because to manage the size of float bits, originally divide by 1024
        mq5 = (str)(temp/10)
        print("MQ5 at location 1 from plant 2: "+mq5)
        if temp > threshold:
            print("###ALERT MESSAGE: THRESHOLD VALUE EXCEEDED###")
            alert = 1
        temp = (grovepi.analogRead(mq2_1sensor)/102.4)
        #temp = gpio.input(18)
        mq2_1 = (str)(temp/10)
        print("MQ2: "+mq2_1)
        if temp > threshold:
            print("###ALERT MESSAGE: THRESHOLD VALUE EXCEEDED###")
            alert = 2
        mq2_2 = (str)(temp/10)
        print("MQ2: "+mq2_2)
        if temp > threshold:
            print("###ALERT MESSAGE: THRESHOLD VALUE EXCEEDED###")
            alert = 3
        time.sleep(1.5)
    except IOError:
        mq5 = 'error'
        print("MQ5: "+mq5)
        mq2_1 = 'error'
        print("MQ2_1: "+mq2_1)
        mq2_2 = 'error'
        print("MQ2_2: "+mq2_2)
    with con:
        cur = con.cursor()
        cur.execute("Insert into node1(Time,MQ5)""values(now(),%s)",(mq5))
        cur.execute("Insert into node2(Time,MQ2)""values(now(),%s)",(mq2_1))
        cur.execute("Insert into node3(Time,MQ2)""values(now(),%s)",(mq2_2))
        if alert == 1:
            cur.execute("Insert into Readings(Time, Node1, Node2, Node3)""values(now(),'Positive','Negitive','Negitive')")
        elif alert == 2:
            cur.execute("Insert into Readings(Time, Node1, Node2, Node3)""values(now(),'Negitive','Positive','Negitive')")
        elif alert == 3:
            cur.execute("Insert into Readings(Time, Node1, Node2, Node3)""values(now(),'Negitive','Negitive','Positive')")
        elif alert == 0:
            cur.execute("Insert into Readings(Time, Node1, Node2, Node3)""values(now(),'Negitive','Negitive','Negitive')")
    #if (count > 0):
     #   time.sleep(2)
    #count = count + 1
    time.sleep(tim)
