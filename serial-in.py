import json
import requests
import random
import serial
import time

# Set these variables :

SERIAL_PORT = ''
BAUD_RATE = 9600


ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)


while True:
    serial_data = ser.readline()
    data = serial_data.split('-')
    sensor_one = str(data[0])
    sensor_two = str(data[1])
    sensor_three = str(data[2])
    print(sensor_one, sensor_two, sensor_three)
    time.sleep(1)
    
