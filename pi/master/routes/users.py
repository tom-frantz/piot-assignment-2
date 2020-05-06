from flask_restful import reqparse, abort, Resource
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from master import app, api
from sqlalchemy.exc import SQLAlchemyError
from master.models import users

# import sys

parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument('username', required=True)
parser.add_argument('password', required=True)
parser.add_argument('first_name', required=True)
parser.add_argument('last_name', required=True)
parser.add_argument('email', required=True)
username = ['a', 'b', 'c']


def check_duplicate_user(user):
    try:
        result = users.UserModel.query.filter_by(username=user).first()
        if result is not None:
            abort(403, message="Username has already been taken.")
    except SQLAlchemyError as e:
        # print("Error:", sys.exc_info()[0])
        error = str(e.__dict__['orig'])
        return {'message': error}, 500


class Register(Resource):
    def post(self):
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']

        check_duplicate_user(username)

        hashed_password = sha256.hash(password)
        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)

        # database new record
        new_user = users.UserModel(
            username=username,
            password=hashed_password,
            first_name=first_name,
            last_name=last_name,
            email=email,
        )
        try:
            new_user.add_new_record()
            return (
                {
                    'username': username,
                    'access_token': access_token,
                    'refresh_token': refresh_token,
                },
                201,
            )
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class Profile(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        print(current_user)
        try:
            result = users.UserModel.query.filter_by(username=current_user).first()
            return {
                'username': result.username,
                'first_name': result.first_name,
                'last_name': result.last_name,
                'email': result.email,
            }
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"Error": error}, 500


api.add_resource(Register, '/users/register')
api.add_resource(Profile, '/users/me')
