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
    flights = collection.find({})
    return render_template('normal_check.html', flights=flights)

if __name__ == '__main__':
    app.run()