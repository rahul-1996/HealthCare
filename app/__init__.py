import os
from flask import Flask
from flask_bootstrap import Bootstrap 
from flask_sqlalchemy import SQLAlchemy 
from celery import Celery
import sqlite3


app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = 'top-secret!'



app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_RESULT_BACKEND'] = 'redis://localhost:6379/0'
#Initialize it
celery = Celery(app.name , broker = app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

db = SQLAlchemy(app)
Bootstrap(app)


app.secret_key = "development in progress"

c = sqlite3.connect('app.db')
cur = c.cursor()
cur.execute("SELECT * from patients")
test = cur.fetchall()




from app import routes, models




