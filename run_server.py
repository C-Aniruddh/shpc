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

    return json.dumps({'s1' : vals_s1, 's2' : vals_s2, 's3' : vals_s3})
    
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


            sensor_one.insert({'id' : sensor_three_id, 'value' : s1_val})
            sensor_two.insert({'id' : sensor_three_id, 'value' : s1_val})
            sensor_three.insert({'id' : sensor_three_id, 'value' : s1_val})

            print(s1_val, s2_val, s3_val)
            time.sleep(2)
    def stop(self):
        self.running = False

if __name__ == "__main__":
    a = SensorValue()
    a.start()
    app.run(host='0.0.0.0', debug=True)