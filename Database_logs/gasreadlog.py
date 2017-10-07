###3 gas sensors connected at A0,A1,A2

import MySQLdb as mdb
import grovepi
import time
import RPi.GPIO as gpio
gpio.setmode(gpio.BOARD)
gpio.setwarnings(False)
mq5sensor = 0
grovepi.pinMode(mq5sensor,"INPUT")
gpio.setup(18,gpio.IN)
#mq2_1sensor = 1
#grovepi.pinMode(mq2_1sensor,"INPUT")
mq2_2sensor = 2
grovepi.pinMode(mq2_2sensor,"INPUT")
count = 0
con=mdb.connect('localhost','user','1234','gas_read');
with con:
    cur = con.cursor()
    #cur.execute("drop table if exists test1")
    cur.execute("create table if not exists gasread(Id Int primary key auto_increment, \
                 tim datetime, mq5 varchar(9), mq2_1 varchar(9), mq2_2 varchar(9))")
while True:
    try:
        temp = (grovepi.analogRead(mq5sensor)/102.4)
        mq5read = (str)(temp/10)
        print("MQ5: "+mq5read)
        #temp = (grovepi.analogRead(mq2_1sensor)/102.4)
	temp = gpio.input(18)
	mq2_1read = (str)(temp/10)
	print("MQ2_1: "+mq2_1read)
	temp = (grovepi.analogRead(mq2_2sensor)/102.4)
        mq2_2read = (str)(temp/10)
        print("MQ2_1: "+mq2_2read)
        time.sleep(1.5)
    except IOError:
        mq5read = 'error'
	print("MQ5: "+mq5read)
	mq2_1read = 'error'
	print("MQ2_1: "+mq2_1read)
	mq2_2read = 'error'
	print("MQ2_2: "+mq2_2read)        
    with con:
        cur = con.cursor()
        cur.execute("Insert into gasread(tim, mq5, mq2_1, mq2_2)""values(now(),%s,%s,%s)",(mq5read,mq2_1read,mq2_2read))
    if(count > 0):
	time.sleep(10*60)
    count = count + 1
