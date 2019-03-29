import json
import requests
import random
import serial
import time

# Set these variables :

SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600


ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)

while True:
    s1_val = random.randint(10, 200)
    s2_val = random.randint(10, 200)
    s3_val = random.randint(10, 200)
    data = "%s-%s-%s" % (s1_val, s2_val, s3_val)
    data = data.encode('utf-8')
    print(s1_val, s2_val, s3_val)
    ser.write(bytes(data))
    time.sleep(2)
    
