from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_socketio import SocketIO
import os


app = Flask(__name__)
# app.config.from_object('config.Config')

# secret_key = os.environ["My_SQL"]
# 'sqlite:///./car_share.db'
app.config[
    'SQLALCHEMY_DATABASE_URI'
] = 'mysql+pymysql://root:1234567@35.193.95.10:3306/IoT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# app.config['SECRET_KEY'] = '1234567' # os.environ['MY_SQL']

app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
# app.config['JWT_BLACKLIST_ENABLED'] = True
# app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']

CORS(app)
api = Api(app)
jwt = JWTManager(app)

db = SQLAlchemy(app)
socketio = SocketIO(app)


# Import of route modules must come after the application object is created
import master.routes.home
import master.routes.users
import master.routes.auth
import master.routes.logout

import master.sockets


@app.before_first_request
def bfr():
    db.drop_all()
    db.create_all()
