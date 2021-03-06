###test1

import MySQLdb as mdb
import grovepi
import time

gas_sensor = 0
grovepi.pinMode(gas_sensor,"INPUT")
moisture_sensor = 1
grovepi.pinMode(moisture_sensor,"INPUT")


con=mdb.connect('localhost','V','v123','vdb');
with con:
    cur = con.cursor()
    #cur.execute("drop table if exists test1")
    cur.execute("create table if not exists test1(Id Int primary key auto_increment, \
                 tim datetime, gval varchar(7), mval varchar(2))")
while True:
    try:
        gas1 = (grovepi.analogRead(gas_sensor)/102.4)
        print(gas1)
        moi1 = grovepi.analogRead(moisture_sensor)
        print(moi1)
        gas = (str)(gas1/10)
        print("G:"+gas)
        moi = (str)(moi1)
        print("M:"+moi)
        time.sleep(1.5)
    except IOError:
        gas = 'error'
        print("G:"+gas)
        moi = 'error'
        print("M:"+moi)
        
    with con:
        cur = con.cursor()
        cur.execute("Insert into test1(tim,gval, mval)""values(now(),%s,%s)",(gas,moi))
    
