from flask_restful import reqparse, abort, Resource
from flask_jwt_extended import (create_access_token, create_refresh_token, jwt_refresh_token_required, get_jwt_identity)
from passlib.hash import pbkdf2_sha256 as sha256
from master import app, api


parser = reqparse.RequestParser()
parser.add_argument('username', required=True)
parser.add_argument('password', required=True)
username = ['a', 'b', 'c']


def user_not_found(user):
    if user not in username:
        abort(401, message='Auth failed.')

def user_password_failure(password, hash):
    #TODO check in database
    if not sha256.verify(password, hash):
        abort(401, message='Wrong password.')

class AccessToken(Resource):
    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        user_not_found(username)

        hash = sha256.hash(password)
        user_password_failure(password, hash)

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return {'username': username, 'access toke ': access_token}, 201

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity() # extract identity from refresh token
        access_token = create_access_token(identity = current_user)
        return {'access_token': access_token}


# api = Api(app)
api.add_resource(AccessToken, '/auth/new')
api.add_resource(TokenRefresh, '/auth/refresh')
