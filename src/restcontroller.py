from re import S, T
import pymongo
import time
import certifi
from datetime import date
from datetime import datetime
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap

ca = certifi.where()
collection = pymongo.MongoClient('mongodb+srv://admin234:274373800@cluster0.o2rcwid.mongodb.net/?retryWrites=true&w=majority', tlsCAFile=ca).user.admin_user

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
    flights = collection.find()
    return render_template('normal_check.html', flights=flights)

# check and edit page for all the flights(admin users)
@app.route('/check_ad', methods=['GET', 'POST'])
def check_admin():
    flights = collection.find()
    if request.method == 'POST':
        json_data = request.form
        if(json_data.get('AddFlight') == 'true'):
            cur = collection.find().sort('_id',-1).limit(1)
            for i in cur:
                id = i["_id"] + 1
            if json_data.get('AddFlightName')!='':
                flight_str = str(json_data.get('AddFlightName'))
            else:
                return render_template('admin_check.html', flights=flights, ADD=True)
            if json_data.get('AddAircraft')!='':
                aircraft_str = str(json_data.get('AddAircraft'))
            else:
                return render_template('admin_check.html', flights=flights, ADD=True)
            if json_data.get('AddDepartPort')!='':
                depart_port_str = str(json_data.get('AddDepartPort'))
            else:
                return render_template('admin_check.html', flights=flights, ADD=True)
            if json_data.get('AddArrivePort')!='':
                arrive_port_str = str(json_data.get('AddArrivePort'))
            else:
                return render_template('admin_check.html', flights=flights, ADD=True)
            if json_data.get('AddDepartTime')!='':
                depart_time_str = str(json_data.get('AddDepartTime'))
            else:
                return render_template('admin_check.html', flights=flights, ADD=True)
            if json_data.get('AddArriveTime')!='':
                arrive_time_str = str(json_data.get('AddArriveTime'))
            else:
                return render_template('admin_check.html', flights=flights, ADD=True)
            try:
                depart_date = datetime.strptime(depart_time_str, "%Y/%m/%d %H:%M:%S")
                arrive_date = datetime.strptime(arrive_time_str, "%Y/%m/%d %H:%M:%S")
                if(arrive_date > depart_date):
                    duration_str = str(arrive_date - depart_date)
                else:
                    return render_template('admin_check.html', flights=flights, date=True)
            except:
                return render_template('admin_check.html', flights=flights, date=True)
            cur = {"_id":id, "flight":flight_str, "aircraft":aircraft_str, 
            "depart_port":depart_port_str, "arrive_port":arrive_port_str, 
            "depart_time":depart_time_str, "arrive_time":arrive_time_str, 
            "duration":duration_str}
            collection.insert_one(cur)
            return render_template('admin_check.html', flights=flights, ADDcom=True)
        else:
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
                    else:
                        return render_template('admin_check.html', flights=flights, date=True)
                except:
                    return render_template('admin_check.html', flights=flights, date=True)
            result = collection.update_one({'_id':pos}, {'$set': cur})
            if result.matched_count == 1:
                return render_template('admin_check.html', flights=flights, update=True)
    return render_template('admin_check.html', flights=flights, date=False)

if __name__ == '__main__':
    app.run()