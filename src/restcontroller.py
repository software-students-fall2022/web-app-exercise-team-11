from re import S
import pymongo
import time
from datetime import date
from datetime import datetime
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

collection = pymongo.MongoClient('mongodb+srv://admin234:274373800@cluster0.o2rcwid.mongodb.net/?retryWrites=true&w=majority').user.admin_user

app = Flask(__name__)
bootstrap=Bootstrap(app)

# home page for our application
@app.route('/')
def home():
    return render_template('home.html')

# check page for all the flights(normal users)
@app.route('/check')
def check():
    flights = collection.find({})
    return render_template('normal_check.html', flights=flights)

# check page for all the flights(admin users)
@app.route('/check_ad', methods=['GET', 'POST'])
def check_admin():
    flights = collection.find({})
    if request.method == 'POST':
        json_data = request.form
        print(json_data)
    return render_template('admin_check.html', flights=flights)

if __name__ == '__main__':
    app.run()