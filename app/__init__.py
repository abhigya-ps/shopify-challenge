from flask import Flask
from flask_sqlalchemy import SQLAlchemy     

app = Flask(__name__)

# set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# import view functions of different url routes ex. /home, /favorites
from app import routes