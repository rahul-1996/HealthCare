from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from app import app
from app import db
from twilio.rest import TwilioRestClient
import schedule
import time

from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class sms_handler:
  def __init__(self,to_name,to_number,med_name):
    self.to_name = to_name
    self.to_number=to_number
    self.med_name=med_name

  def send_sms(self):
    twilio_account={'account_sid':'AC38383c8745364aea790822b5a7b1a9b5','auth_token':'91f42bbf0c3a5b5b3d4536a1e1cf9f0a'}
    client= TwilioRestClient(twilio_account['account_sid'],twilio_account['auth_token'])
    message=client.messages.create(to=self.to_number,from_="+15594219414",body='Hey '+self.to_name+' time to take ' + self.med_name)
  
  def automate(self):
    schedule.every(1).minutes.do(self.send_sms)
    while True:
      schedule.run_pending()
      time.sleep(1)

      

class User(db.Model):
  __tablename__ = 'users'
  uid = db.Column(db.Integer, primary_key = True)
  firstname = db.Column(db.String(100))
  lastname = db.Column(db.String(100))
  email = db.Column(db.String(120) )
  pwdhash = db.Column(db.String(54))
  patients = db.relationship('Patient', backref = "user" , lazy = 'dynamic')
   
  def __init__(self, firstname, lastname, email, password):
    self.firstname = firstname.title()
    self.lastname = lastname.title()
    self.email = email.lower()
    self.set_password(password)
     
  def set_password(self, password):
    self.pwdhash = generate_password_hash(password)
   
  def check_password(self, password):
    return check_password_hash(self.pwdhash, password)  


class Patient(db.Model) :
  __tablename__ = 'patients'
  uid = db.Column(db.Integer , primary_key = True ,autoincrement=True)
  name = db.Column(db.String(100) , nullable = False , index = True)
  phone = db.Column(db.String(15)   , nullable = False )
  patient_id = db.Column(db.Integer ,db.ForeignKey('users.uid') )
  medicines = db.Column(db.String(100))
  time = db.Column(db.String(10))

  def __init__(self , name , phone , medicines , time) :
    self.name = name
    self.phone = phone
    self.medicines = medicines
    self.time = time





