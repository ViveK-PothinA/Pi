import serial, time
import MySQLdb as mdb
ser = serial.Serial("/dev/ttyACM0",9600)
con=mdb.connect('localhost','user','1234','gas_read');
with con:
    cur = con.cursor()
    #cur.execute("drop table if exists test1")
    cur.execute("create table if not exists ard1(Id Int primary key auto_increment, \
                 tim datetime, mq2 varchar(9))")
while True:
    read = ""
    #for i in range(0,4):
    read = ser.readline()
    print(read)
    #read1 = read/102.4
    #read = str(read1/10)
    with con:
        cur = con.cursor()
        cur.execute("Insert into ard1(tim, mq2)""values(now(),%s)",(read))
    time.sleep(10)
