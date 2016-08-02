from flask import Flask
from flask_bootstrap import Bootstrap 
from app.models import db

app = Flask(__name__)
Bootstrap(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root123@localhost/users'
 
db.init_app(app)

app.secret_key = "development in progress"

from app import routes, models

