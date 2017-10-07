#!/usr/bin/env python
#
# GrovePi Example for using the  Grove Gas Sensor
#
# The GrovePi connects the Raspberry Pi and Grove sensors.  You can learn more about GrovePi here:  http://www.dexterindustries.com/GrovePi
#
# Have a question about this example?  Ask on the forums here:  http://forum.dexterindustries.com/c/grovepi
#
'''
## License

The MIT License (MIT)

GrovePi for the Raspberry Pi: an open source platform for connecting Grove Sensors to the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

# NOTE:
# There are 5 gas sensors
# MQ2 - Combustible Gas, Smoke
# MQ3 - Alcohol Vapor
# MQ5 - LPG, Natural Gas, Town Gas
# MQ9 - Carbon Monoxide, Coal Gas, Liquefied Gas
# 02 - Oxygen
# The sensitivity can be adjusted by the onboard potentiometer
#
# http://www.seeedstudio.com/wiki/Grove_-_Gas_Sensor
# http://www.seeedstudio.com/wiki/Grove_-_Gas_Sensor(MQ5)
# http://www.seeedstudio.com/wiki/Grove_-_Gas_Sensor(O%E2%82%82)
from __future__ import print_function
import paho.mqtt.publish as publish
import psutil

import time
import grovepi
import httplib,urllib
sleep = 15 # how many seconds to sleep between posts to the channel
channelID = "216875"
apiKey = '4QRA81L6FRDBNZOO'  # Thingspeak channel to update httplib,
useUnsecuredTCP = False
useUnsecuredWebsockets = False
useSSLWebsockets = True
mqttHost = "mqtt.thingspeak.com"
# Set up the connection parameters based on the connection type
if useUnsecuredTCP:
    tTransport = "tcp"
    tPort = 1883
    tTLS = None
    print(tPort)
if useUnsecuredWebsockets:
    tTransport = "websockets"
    tPort = 80
    tTLS = None
    print(tPort)
if useSSLWebsockets:
    import ssl
    tTransport = "websockets"
    tTLS = {'ca_certs':"/etc/ssl/certs/ca-certificates.crt",'tls_version':ssl.PROTOCOL_TLSv1}
    tPort = 443
    print(tPort)   
# Create the topic string
topic = "channels/" + channelID + "/publish/" + apiKey
# Connect the Grove Gas Sensor to analog port A0
# SIG,NC,VCC,GND
gas_sensor = 0

grovepi.pinMode(gas_sensor,"INPUT")

while True:
    try:
        # Get sensor value
        sensor_value = grovepi.analogRead(gas_sensor)
        tPayload = "Reading=" + str(sensor_value)
        print(tPayload)
        # attempt to publish this data to the topic 
        try:
            publish.single(topic, payload=tPayload, hostname=mqttHost, port=tPort, tls=tTLS, transport=tTransport)
            print("success")
        except (KeyboardInterrupt):
            break

        except:
            print ("There was an error while publishing the data.")

        # Calculate gas density - large value means more dense gas
        #density = (float)(sensor_value / 1024)

        #print("sensor_value =", sensor_value, " density =", density)
        #time.sleep(.5)
        time.sleep(sleep)
    except IOError:
        print ("Error")
