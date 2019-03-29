from flask import Flask, render_template, url_for, request, session, redirect, send_from_directory, jsonify
import os
from flask_pymongo import PyMongo
import bcrypt
import datetime
import time
import json
import timeago
from bson.json_util import dumps

import numpy as np
import pandas as pd

import io
import json

import glob
from werkzeug.utils import secure_filename
import threading 

from threading import Thread

import zipfile

import random
import cv2

import serial


app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config['MONGO_DBNAME'] = 'minor'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/minor'

app.secret_key = 'mysecret'


mongo = PyMongo(app)


@app.route('/')
def index():
    sensor_one = mongo.db.sensor_one
    sensor_two = mongo.db.sensor_two
    sensor_three = mongo.db.sensor_three

    find_all_s1 = sensor_one.find({})
    ids_s1 = []
    vals_s1 = []
    for s in find_all_s1:
        ids_s1.append(s['id'])
        vals_s1.append(str(s['value']))

    find_all_s2 = sensor_two.find({})
    ids_s2 = []
    vals_s2 = []
    for s in find_all_s2:
        ids_s2.append(s['id'])
        vals_s2.append(str(s['value']))

    find_all_s3 = sensor_three.find({})
    ids_s3 = []
    vals_s3 = []
    for s in find_all_s3:
        ids_s3.append(s['id'])
        vals_s3.append(str(s['value']))


    return render_template('app/dashboard.html', id_list=ids_s1, data_list_s1=vals_s1[-12:], data_list_s2=vals_s2[-12:], data_list_s3=vals_s3[-12:] )
   

@app.route('/get_data')
def get_data():
    sensor_one = mongo.db.sensor_one
    sensor_two = mongo.db.sensor_two
    sensor_three = mongo.db.sensor_three

    find_all_s1 = sensor_one.find({})
    ids_s1 = []
    vals_s1 = []
    for s in find_all_s1:
        ids_s1.append(s['id'])
        vals_s1.append(str(s['value']))

    find_all_s2 = sensor_two.find({})
    ids_s2 = []
    vals_s2 = []
    for s in find_all_s2:
        ids_s2.append(s['id'])
        vals_s2.append(str(s['value']))

    find_all_s3 = sensor_three.find({})
    ids_s3 = []
    vals_s3 = []
    for s in find_all_s3:
        ids_s3.append(s['id'])
        vals_s3.append(str(s['value']))

    print(vals_s1[-12:])
    print(vals_s2[-12:])
    return json.dumps({'s1' : vals_s1[-12:], 's2' : vals_s2[-12:], 's3' : vals_s3[-12:]})
    

@app.route('/get_total')
def get_total():
    sensor_one = mongo.db.sensor_one
    sensor_two = mongo.db.sensor_two
    sensor_three = mongo.db.sensor_three

    find_all_s1 = sensor_one.find({})
    find_all_s2 = sensor_two.find({})
    find_all_s3 = sensor_three.find({})

    find_all_s1_c = find_all_s1.count()
    find_all_s2_c = find_all_s2.count()
    find_all_s3_c = find_all_s3.count()

    total = find_all_s1_c + find_all_s2_c + find_all_s3_c

    return json.dumps({'result' : total})

@app.route('/get_avg')
def get_avg():
    sensor_one = mongo.db.sensor_one
    sensor_two = mongo.db.sensor_two
    sensor_three = mongo.db.sensor_three

    find_all_s1 = sensor_one.find({})
    ids_s1 = []
    vals_s1 = []
    for s in find_all_s1:
        ids_s1.append(s['id'])
        vals_s1.append(str(s['value']))

    find_all_s2 = sensor_two.find({})
    ids_s2 = []
    vals_s2 = []
    for s in find_all_s2:
        ids_s2.append(s['id'])
        vals_s2.append(str(s['value']))

    find_all_s3 = sensor_three.find({})
    ids_s3 = []
    vals_s3 = []
    for s in find_all_s3:
        ids_s3.append(s['id'])
        vals_s3.append(str(s['value']))

    total = int(vals_s1[-1]) + int(vals_s2[-1]) + int(vals_s3[-1]) 

    return json.dumps({'result' : total//3})
    

@app.route('/get_s1')
def get_s1():
    sensor_one = mongo.db.sensor_one
    find_all_s1 = sensor_one.find({})
    ids_s1 = []
    vals_s1 = []
    for s in find_all_s1:
        ids_s1.append(s['id'])
        vals_s1.append(str(s['value']))
    return json.dumps({'result' : vals_s1[-1]})


@app.route('/get_s2')
def get_s2():
    sensor_two = mongo.db.sensor_two
    find_all_s2 = sensor_two.find({})
    ids_s2 = []
    vals_s2 = []
    for s in find_all_s2:
        ids_s2.append(s['id'])
        vals_s2.append(str(s['value']))

    return json.dumps({'result' : vals_s2[-1]})



@app.route('/get_s3')
def get_s3():
    sensor_three = mongo.db.sensor_three
    find_all_s3 = sensor_three.find({})
    ids_s3 = []
    vals_s3 = []
    for s in find_all_s3:
        ids_s3.append(s['id'])
        vals_s3.append(str(s['value']))

    return json.dumps({'result' : vals_s3[-1]})


class SensorValue(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.running = True

    def run(self):
        while self.running:        
            sensor_one = mongo.db.sensor_one
            sensor_two = mongo.db.sensor_two
            sensor_three = mongo.db.sensor_three

            s1_val = random.randint(10, 200)
            s2_val = random.randint(10, 200)
            s3_val = random.randint(10, 200)

            sensor_one_f = sensor_one.find({})
            sensor_one_c = sensor_one_f.count()
            sensor_one_id = str(sensor_one_c + 1)


            sensor_two_f = sensor_two.find({})
            sensor_two_c = sensor_two_f.count()
            sensor_two_id = str(sensor_two_c + 1)


            sensor_three_f = sensor_three.find({})
            sensor_three_c = sensor_one_f.count()
            sensor_three_id = str(sensor_three_c + 1)


            sensor_one.insert({'id' : sensor_one_id, 'value' : s1_val})
            sensor_two.insert({'id' : sensor_two_id, 'value' : s2_val})
            sensor_three.insert({'id' : sensor_three_id, 'value' : s3_val})

            print(s1_val, s2_val, s3_val)
            time.sleep(2)
    def stop(self):
        self.running = False


class serialRead(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        self.running = True

    def run(self):
        while self.running:        
            sensor_one = mongo.db.sensor_one
            sensor_two = mongo.db.sensor_two
            sensor_three = mongo.db.sensor_three

            serial_data = self.ser.readline()
            reading = ''
            reading = serial_data.decode('utf-8').rstrip()
            print(reading)
            if len(reading) > 0:
                
                data = reading.split('-')
                print(data)
                s1_val = str(data[0])
                s2_val = str(data[1])
                s3_val = str(data[2])
                print("Received", s1_val, s2_val, s3_val)
                

                sensor_one_f = sensor_one.find({})
                sensor_one_c = sensor_one_f.count()
                sensor_one_id = str(sensor_one_c + 1)


                sensor_two_f = sensor_two.find({})
                sensor_two_c = sensor_two_f.count()
                sensor_two_id = str(sensor_two_c + 1)


                sensor_three_f = sensor_three.find({})
                sensor_three_c = sensor_three_f.count()
                sensor_three_id = str(sensor_three_c + 1)


                sensor_one.insert({'id' : sensor_one_id, 'value' : s1_val})
                sensor_two.insert({'id' : sensor_two_id, 'value' : s2_val})
                sensor_three.insert({'id' : sensor_three_id, 'value' : s3_val})

                print(s1_val, s2_val, s3_val)
            time.sleep(1)

    def stop(self):
        self.running = False


if __name__ == "__main__":
    #a = SensorValue()
    a = serialRead()
    a.start()
    app.run(host='0.0.0.0', debug=True)