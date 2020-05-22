from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
import master.config
import os

app = Flask(__name__)

# load config
if os.environ['FLASK_ENV'] == "testing":
    app.config.from_object('master.config.TestingConfig')
elif os.environ['FLASK_ENV'] == "production":
    app.config.from_object('master.config.ProductionConfig')
else:
    app.config.from_object('master.config.DevelopmentConfig')

# load extentions
CORS(app)
api = Api(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)
socketio = SocketIO(app)

# !! ATTENTTION !!
# Import of route modules must come after the application object is created
import master.routes.home
import master.routes.users
import master.routes.auth
import master.routes.cars
import master.routes.bookings

import master.sockets


# create database (if not exist) before first api request
@app.before_first_request
def create_tables():
    if app.config['TESTING'] == False:
        db.drop_all()
        db.create_all()
