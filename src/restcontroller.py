# from django.shortcuts import render
import pymongo
import time
from datetime import date
from datetime import datetime
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

# collection = pymongo.MongoClient('localhost', 27017).admin.test
collection = pymongo.MongoClient('mongodb+srv://admin234:274373800@cluster0.o2rcwid.mongodb.net/?retryWrites=true&w=majority').user.admin_user

app = Flask(__name__)
bootstrap=Bootstrap(app)

# home page for our application
@app.route('/')
def home():
    return render_template('home.html')

# check page for all the flights
@app.route('/check')
def check():
    return render_template('check.html')
# d1 = datetime(2022, 12, 28, 6, 17, 42)
# d2 = datetime(2022, 12, 28, 10, 23, 19)
# d3 = d2-d1
# s1 = d1.strftime('%Y/%m/%d %H:%M:%S')
# s2 = d2.strftime('%Y/%m/%d %H:%M:%S')
# s3 = str(d3)

# d = {"_id":4, "flight": "BY0072P", "aircraft":"A220-300", 
# "depart_port":"MPTO ", "arrive_port":"KLAX", 
# "depart_time":s1, "arrive_time":s2, 
# "duration":s3}
# collection.insert_one(d)

if __name__ == '__main__':
    app.run()