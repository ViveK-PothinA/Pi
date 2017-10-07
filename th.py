import grovepi
while True:
    [temp, humidity] = grovepi.dht(5, 0)
    print(temp, humidity)


    
   
