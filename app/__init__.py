from flask import Flask
from flask_sqlalchemy import SQLAlchemy     

app = Flask(__name__)

# set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from app import routes