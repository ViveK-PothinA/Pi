import MySQLdb as mdb
import grovepi
import time
mq5sensor = 0           #connect to A0
grovepi.pinMode(mq5sensor,"INPUT")
moisture_sensor = 1         #connect to A1
grovepi.pinMode(moisture_sensor,"INPUT")
dhtsensor = 4               #connet temperature and humidity sensor at digital port 4
###replace these values by the threshold values for each sensor
gas_threshold = 10
gasleak_threshold = 1000
moisture_threshold = -10
temp_threshold = 52
temp_alert = False
gas_alert = False
shutdown = False
pump_water = False
#SET THE REQUIRED INTERVAL
interval = 1*10
#Connecting to the database
try:
    con = mdb.connect('localhost','user1','1234','readings');
except:
    print("Couldn't connect to the database")
    shutdown = True
#Functions for getting data from sensors
def checkgas():
    try:
        val = (grovepi.analogRead(mq5sensor)/102.4)
        mq5 = str(val/10)
    except(IOError):
        mq5 = "NAN"
    print("MQ5 at Node *: " + mq5)
    if val > gasleak_threshold:
        print("###ALERT AT NODE *: SYSTEM SHUTDOWN")
        shutdownflag = True
        #exit(0)
        return mq5, True,shutdownflag
    elif val > gas_threshold:
        print("###ALERT AT NODE *: MQ5 THRESHOLD VALUE EXCEEDED###")
        alert = True
        return mq5, alert, False
    else:
        return mq5,False, False
def checkmoi(shutdownflag):
    try:
        val = grovepi.analogRead(moisture_sensor)
        moi = str(val)
    except(IOError):
        moi = "NAN"
    print("Moisture content at Node *: " + moi)
    if val < moisture_threshold and not shutdownflag:
        print("###WATER LOW, PUMPING WATER###")
        alert = True
        time.sleep(10)
        return checkmoi(shutdownflag)
    return moi,False
def checktemphum():
    try:
        [valt,valh] = grovepi.dht(dhtsensor,0)
        temperature = str(valt)
        humidity = str(valh)
    except(IOError):
        temperature = "NAN"
        humidity = "NAN"
    print("Temperature and Humidity at Node *: " + temperature + ", " + humidity)
    try:
        val = (valt - (100 - valh)/5)
        reference = str(val)
    except:
        reference = "NAN"
    print("Reference value at Node *: " + reference)
    if valt > temp_threshold:
        print("###ALERT AT NODE *: TEMPERATURE THRESHOLD EXCEEDED")
        alert = True
        return temperature, humidity, reference, alert
    return temperature, humidity,reference, False
#Main Loop
while (not shutdown):
    #resets every time
    #print(shutdown)
    gas_alert = False
    gas_leak = False
    pump_water = False
    #Collect data
    [mq5, gas_alert, shutdown] = checkgas() 
    [moi, pump_water] = checkmoi(shutdown)
    [temperature, humidity, reference, temp_alert] = checktemphum()
    #Storing to database
    with con:
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS Data1(Time datetime, Temp varchar(9),\
Humidity varchar(9), Moisture varchar(9), MQ5 varchar(9),Reference varchar(9))")
        cur.execute("INSERT INTO Data1(Time, Temp, Humidity, Moisture, Mq5, Reference)""\
values(now(), %s, %s, %s, %s, %s)",(temperature, humidity, moi, mq5, reference))
    if gas_alert:
        time.sleep(10)
    continue
    time.sleep(interval)


    
