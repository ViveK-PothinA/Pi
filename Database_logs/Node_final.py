###Gas sensors connected at A0
###Soil Moisture sensor connected at A1
# 	Sensor values observer: 
# 		Val  Condition
# 		0    sensor in open air
# 		18   sensor in dry soil
# 		425  sensor in humid soil
# 		690  sensor in water
import MySQLdb as mdb
import grovepi
import time
mq5sensor = 0           #connect to A0
grovepi.pinMode(mq5sensor,"INPUT")
moisture_sensor = 1         #connect to A1
grovepi.pinMode(moisture_sensor,"INPUT")
###replace these values by the threshold values for each sensor
gas_threshold = 10
gasleak_threshold = 20
moisture_threshold = 100
tim = 2     #time to delay
con=mdb.connect('localhost','user','1234','gas_read');
with con:
    cur = con.cursor()
    cur.execute("create table if not exists Readings(Time datetime,Node1 varchar(9),Node2 varchar(9),Node3 varchar(9))")
while True:
    gas_alert = False           #resets every time
    gas_leak = False
    pump_water = False
    try:
        temp = (grovepi.analogRead(mq5sensor)/102.4) #divide by 102.4 because to manage the size of float bits, originally divide by 1024
        mq5 = (str)(temp/10)
        print("MQ5 at location 1 from plant 2: "+mq5)
        if temp > threshold:
            print("###ALERT MESSAGE: THRESHOLD VALUE EXCEEDED###")
            alert = 1
        temp = grovepi.analogRead(mq2_1sensor)
        moisture = str(temp)
        print("Moisture: "+moisture)
        if temp < moisture_threshold:
            print("###LESS WATER, PUMP WATER###")
            pump_water = 1
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
