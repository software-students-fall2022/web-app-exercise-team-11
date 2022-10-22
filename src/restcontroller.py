from re import S, T
import pymongo
import time
from datetime import date
from datetime import datetime
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
# from flask_datepicker import datepicker
# from wtforms.fields import DateField

collection = pymongo.MongoClient('mongodb+srv://admin234:274373800@cluster0.o2rcwid.mongodb.net/?retryWrites=true&w=majority').user.admin_user

app = Flask(__name__)
bootstrap=Bootstrap(app)

# home page for our application
@app.route('/')
def home():
    return render_template('home.html')
    # return render_template('test.html')

# check page for all the flights(normal users)
@app.route('/check')
def check():
    flights = collection.find({})
    return render_template('normal_check.html', flights=flights)

# check and edit page for all the flights(admin users)
@app.route('/check_ad', methods=['GET', 'POST'])
def check_admin():
    flights = collection.find({})
    if request.method == 'POST':
        json_data = request.form
        pos = int(json_data.get('InputID'))
        cur = collection.find_one({'_id':pos})
        if json_data.get('InputFlightName')!='':
            cur['flight'] = str(json_data.get('InputFlightName'))
        if json_data.get('InputAircraft')!='':
            cur['aircraft'] = str(json_data.get('InputAircraft'))
        if json_data.get('InputDepartPort')!='':
            cur['depart_port'] = str(json_data.get('InputDepartPort'))
        if json_data.get('InputArrivePort')!='':
            cur['arrive_port'] = str(json_data.get('InputArrivePort'))
        if json_data.get('InputDepartTime')!='':
            depart_str = str(json_data.get('InputDepartTime'))
            try:
                depart_date = datetime.strptime(depart_str, "%Y/%m/%d %H:%M:%S")
                cur['depart_time'] = depart_str
                arrive_str = ""
                if json_data.get('InputArriveTime')!='':
                    arrive_str = str(json_data.get('InputArriveTime'))
                    cur['arrive_time'] = arrive_str
                else:
                    arrive_str = str(cur['arrive_time'])
                arrive_date = datetime.strptime(arrive_str, "%Y/%m/%d %H:%M:%S")
                if(arrive_date > depart_date):
                    duration_str = str(arrive_date - depart_date)
                    cur['duration'] = duration_str
                    result = collection.update_one({'_id':pos}, {'$set': cur})
                    if result.matched_count == 1:
                        return render_template('admin_check.html', flights=flights, update=True)
                else:
                    return render_template('admin_check.html', flights=flights, date=True)
            except:
                return render_template('admin_check.html', flights=flights, date=True)
        elif json_data.get('InputArriveTime')!='':
            arrive_str = str(json_data.get('InputArriveTime'))
            try:
                arrive_date = datetime.strptime(arrive_str, "%Y/%m/%d %H:%M:%S")
                cur['arrive_time'] = arrive_str
                depart_date = datetime.strptime(cur['depart_time'], "%Y/%m/%d %H:%M:%S")
                if(arrive_date > depart_date):
                    duration_str = str(arrive_date - depart_date)
                    cur['duration'] = duration_str
                    result = collection.update_one({'_id':pos}, {'$set': cur})
                    if result.matched_count == 1:
                        return render_template('admin_check.html', flights=flights, update=True)
                else:
                    return render_template('admin_check.html', flights=flights, date=True)
            except:
                return render_template('admin_check.html', flights=flights, date=True)
    return render_template('admin_check.html', flights=flights, date=False)

if __name__ == '__main__':
    app.run()