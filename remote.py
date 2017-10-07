import urllib, serial
ser = serial.Serial('/dev/ttyACM0', 9600)

dir = 0
while True:
    site = urllib.urlopen('http://remotebot.rcssastra.com/answer.txt').read()

    print site

    print(type(site))
    print site[0]

    dir = int(site[0])

    if dir is 0:
        ser.write('0'b)

    elif dir is 1:
        ser.write('1'b)

    elif dir is 2:
        ser.write('2'b)

    elif dir is 3:
        ser.write('3'b)

    elif dir is 4:
        ser.write('4'b)
