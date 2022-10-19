import pymongo
from flask import Flask, render_template
from flask_bootstrap import Bootstrap

collection = pymongo.MongoClient('localhost', 27017).admin.test

app = Flask(__name__)
# Bootstrap(app) try
bootstrap=Bootstrap(app)
  
# home page for our application
@app.route('/')
def index():
    return render_template('base.html')
    # return render_template('home.html')

# d = {"DP510": 12}

# collection.insert_one(d)

if __name__ == '__main__':
    app.run()