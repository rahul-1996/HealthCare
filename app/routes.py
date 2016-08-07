from app import app , db , celery , test
from flask import Flask, render_template, request, flash, session, redirect, url_for , jsonify
from app.models import db , User , Patient , sms_handler
from app.forms import SignupForm , SigninForm , PatientDetails
import time , schedule 
from celery import Celery
from twilio.rest import TwilioRestClient


@celery.task
def ggwp(to_name,to_number,meds):
  smstask=sms_handler(to_name,to_number,meds)
  smstask.automate()

'''
@celery.task
def send_sms(to_name ,to_number,med_name):
    twilio_account={'account_sid':'AC38383c8745364aea790822b5a7b1a9b5','auth_token':'91f42bbf0c3a5b5b3d4536a1e1cf9f0a'}
    client = TwilioRestClient(twilio_account['account_sid'], twilio_account['auth_token'])
    message = client.messages.create(to=to_number, from_="+15594219414",body=med_name) 
    return to_name ,to_number,med_name 
def automate(send_sms,time_set):
        schedule.every().day.at(time_set).do(send_sms)
        while True:
            schedule.run_pending()
            time.sleep(1)

'''

@app.route('/')
def index() :
  return render_template('index.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
  form = SignupForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signup.html', form=form)
    else:   
      newuser = User(form.firstname.data, form.lastname.data, form.email.data, form.password.data)
      db.session.add(newuser)
      db.session.commit()

      session['email'] = newuser.email

      return redirect(url_for('profile'))
   
  elif request.method == 'GET':
    return render_template('signup.html', form=form)

@app.route('/profile')
def profile():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
 
  user = User.query.filter_by(email = session['email']).first()  

 
  if user is None:
    return redirect(url_for('signin'))
  else:
    return render_template('profile.html' , test = test )

@app.route('/patient.html', methods=['GET', 'POST'])
def patient() :

  if 'email' not in session:
    return redirect(url_for('signin'))

  user = User.query.filter_by(email = session['email']).first()  
  form = PatientDetails()
  if request.method == 'POST' :
     if form.validate_on_submit():
        newPatient = Patient(name = form.name.data ,phone = form.phone.data , medicines = form.medicines.data , time = form.time.data)
        failed = False


        try :
          db.session.add(newPatient)
          db.session.commit() 
        except :
          db.session.rollback()
          db.session.flush() # for resetting non-commited .add()
          db.session.add(newPatient)
          db.session.commit()
          failed=True
        
        
        #newsms = sms_handler('+91'+newPatient.phone , 'Take'+ newPatient.medicines + 'in one hour')
        #newsms.automate()
        ggwp.apply_async([newPatient.name,'+91'+newPatient.phone,newPatient.medicines]) 
        flash('Message succesfully sent !')
        return redirect(url_for('profile'))

  elif request.method == 'GET' :
      return render_template('patient.html', form = form )

    
'''
        to_name = newPatient.name 
        to_number = newPatient.phone
        med_name = newPatient.medicines

        automate(send_sms('Hey '+to_name ,'+91'+to_number,'Time to take '+ med_name) , newPatient.time)
        while True:
          schedule.run_pending()
          time.sleep(1)   
'''

 
@app.route('/signin', methods=['GET', 'POST'])
def signin():
  form = SigninForm()
   
  if request.method == 'POST':
    if form.validate() == False:
      return render_template('signin.html', form=form)
    else:
      session['email'] = form.email.data
      return redirect(url_for('profile'))
                 
  elif request.method == 'GET':
    return render_template('signin.html', form=form)

@app.route('/signout')
def signout():
 
  if 'email' not in session:
    return redirect(url_for('signin'))
     
  session.pop('email', None)
  return redirect(url_for('index'))






