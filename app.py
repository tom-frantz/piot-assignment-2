from flask import Flask
from flask_restful import Resource, Api
from test import Home as Home
from register import Register as Register
from auth import Auth as Auth
from logout import Logout as Logout

app = Flask(__name__)
api = Api(app)


api.add_resource(Home, '/')
api.add_resource(Register, '/register')
api.add_resource(Auth, '/auth')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(debug=True)
