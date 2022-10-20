# from django.shortcuts import render
import pymongo
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_simplelogin import SimpleLogin

collection = pymongo.MongoClient('localhost', 27017).admin.test

app = Flask(__name__)
bootstrap=Bootstrap(app)
SimpleLogin(app)
  
# home page for our application
@app.route('/')
def home():
    return render_template('home.html')

# check page for all the flights
@app.route('/check')
def check():
    return render_template('check.html')

# d = {"DP510": 12}

# collection.insert_one(d)

if __name__ == '__main__':
    app.run()