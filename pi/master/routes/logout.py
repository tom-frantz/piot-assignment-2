from flask_restful import reqparse, abort, Resource
from master import app, api

parser = reqparse.RequestParser()
parser.add_argument('username')
username = ['a', 'b', 'c']


class Logout(Resource):
    def post(self):
        args = parser.parse_args()
        new_user = args['username']
        return {'message': "user logged out."}


api.add_resource(Logout, '/logout')
