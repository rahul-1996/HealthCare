#!flask/bin/python
from app import app
from app import db  
app.run(host="0.0.0.0",port=8000,debug=True)
