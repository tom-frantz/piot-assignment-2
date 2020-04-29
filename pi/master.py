from flask import Flask
from flask_restful import Api
from pi.agent.test import Home as Home
from pi.agent.register import Register as Register
from pi.agent.auth import Auth as Auth
from pi.agent.logout import Logout as Logout

app = Flask(__name__)
api = Api(app)


api.add_resource(Home, '/')
api.add_resource(Register, '/register')
api.add_resource(Auth, '/auth')
api.add_resource(Logout, '/logout')

if __name__ == '__main__':
    app.run(debug=True)
