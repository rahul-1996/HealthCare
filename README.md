INSTRUCTIONS TO RUN THIS :

1 . CREATE A VIRTUAL ENVIRONMENT NAMED FLASK ON PYTHON3 .
       This is done by :  python3 -m venv flask
                          source flask/bin/activate

2 . RUN THE FOLLOWING COMMANDS :
      Install the following dependencies :
	      pip install -r requirements.txt
	      pip install schedule
	      pip install redis
	      pip install twilio
	      pip install celery

      Run following commands with the virtual environment activated :
 	     1. chmod a+x db_create.py
		./db_create.py
	     2. chmod a+x run-redis.sh   (HAVE ITS OWN DEDICATED TERMINAL WITH VIRTUAL ENV 			ACTIVATED)
		./run-redis.sh
	     3. (AGAIN ON ITS DEDICATED TERMINAL WITH VIRTUAL ENVIRONMMENT ENABLED)
                 start a Celery worker:
			 flask/bin/celery worker -A app.celery --loglevel=info

 	     4. (AGAIN ON ITS DEDICATED TERMINAL WITH VIRTUAL ENVIRONMMENT ENABLED)
			chmod a+x run.py
			./run.py
 
Go to the localhost now to see an up and running live demo

3. Functionality :
        Only few numbers are verfied with twilio as of now so send a message to '9535242810' to confirm the functionality of the app. 
        Also , the sqlite3 database is fully functioning and can be accessed by the command line.
Could not implement it on the webpage due to restrains in time. 
 We have configured it to send an sms every minute just for testing purposes




	     
