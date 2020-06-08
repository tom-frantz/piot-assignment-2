"""
RESTful API Routes: `/users/{endpoint}`
"""

from flask_restful import reqparse, abort, Resource, inputs
from passlib.hash import pbkdf2_sha256 as sha256
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from master import app, api, db
from sqlalchemy.exc import SQLAlchemyError
from master.models import users, bookings
from master.auth import checkAdmin, checkEngineer
import master.validation as validate

# req parser: add a new user
parser = reqparse.RequestParser(bundle_errors=True)
parser.add_argument(
    'username', type=inputs.regex(r'^[A-Za-z0-9-_]{3,15}$'), required=True
)
parser.add_argument(
    'password', type=inputs.regex(r'^[A-Za-z0-9]{8,30}$'), required=True
)
parser.add_argument(
    'first_name', type=inputs.regex(r'^[A-Za-z0-9-_]{1,30}$'), required=True
)
parser.add_argument(
    'last_name', type=inputs.regex(r'^[A-Za-z0-9-_]{1,30}$'), required=True
)
parser.add_argument(
    'email',
    type=inputs.regex(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,6})$'),
    required=True,
)

# req parser: update user details except password
parser_info = reqparse.RequestParser(bundle_errors=True)
parser_info.add_argument(
    'username', type=inputs.regex(r'^[A-Za-z0-9-_]{3,15}$'), required=True
)
parser_info.add_argument(
    'first_name', type=inputs.regex(r'^[A-Za-z0-9-_]{1,30}$')
)
parser_info.add_argument(
    'last_name', type=inputs.regex(r'^[A-Za-z0-9-_]{1,30}$')
)
parser_info.add_argument(
    'email',
    type=inputs.regex(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,6})$')
)
parser_info.add_argument('role', type=validate.role)

def check_duplicate_user(user):
    """
    Help method in user registration to check if the username is occupied in database.
    """
    try:
        result = users.UserModel.query.filter_by(username=user).first()
        if result is not None:
            abort(403, message="Username has already been taken.")
    except SQLAlchemyError as e:
        #error = str(e.__dict__['orig'])
        return {'message': str(e)}, 500


class Register(Resource):
    """
    New user registration. No admin or engineer account allowed.
    """
    def post(self):
        """
        :param str username: required.
        :param str password: required.
        :param str first_name: required.
        :param str last_name: required.
        :param str email: required.
        """
        args = parser.parse_args()
        username = args['username']
        password = args['password']
        first_name = args['first_name']
        last_name = args['last_name']
        email = args['email']

        check_duplicate_user(username)

        hashed_password = sha256.hash(password)
        user_identity = {'username': username, 'role': 'user'}
        access_token = create_access_token(identity=user_identity)
        refresh_token = create_refresh_token(identity=user_identity)

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
    """
    View current user profile.
    """
    @jwt_required
    def get(self):
        """
        - JWT required.
        - Header: `\"Authorization\": \"Bearer {access_token}\"`
        """
        current_user = get_jwt_identity()
        username = current_user['username']
        try:
            result = users.UserModel.query.filter_by(username=username).first()
            if result is None:
                return {'Error': 'User not found'}, 404
            return {
                'username': result.username,
                'first_name': result.first_name,
                'last_name': result.last_name,
                'email': result.email,
                #'role': result.role
            }
        except SQLAlchemyError as se:
            error = str(se.__dict__['orig'])
            return {"Error": error}, 500

class AllUsers(Resource):
    """
    Get all users with corresponding bookings.
    """
    @jwt_required
    def get(self):
        """
        - JWT required.
        - **Admin only.**
        - Header: `\"Authorization\": \"Bearer {access_token}\"`
        """
        current_user = get_jwt_identity()
        role = current_user["role"]

        checkAdmin(role)

        try:
            all_users = users.UserModel.query.all()

            user_list = []

            for i in all_users:
                user_item = {
                    "username": i.username,
                    "first_name": i.first_name,
                    "last_name": i.last_name,
                    "email": i.email,
                    "role": i.role,
                    "bookings": []
                }
                all_bookings = bookings.BookingModel.query.filter_by(
                    username = i.username
                ).all()
                if len(all_bookings) > 0:
                    booking_list = list(
                        map(
                            lambda i: {
                                'booking_id': i.booking_id,
                                'username': i.username,
                                'departure_time': i.departure_time.isoformat(),
                                'return_time': i.return_time.isoformat(),
                                'created_at': i.created_at.isoformat(),
                            },
                            all_bookings,
                        )
                    )
                    user_item['bookings'] = booking_list
                user_list.append(user_item)

            return user_list, 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500

class ChangeUserDetail(Resource):
    """
    Change user details: first name, last name, and email.
    """
    @jwt_required
    def put(self):
        """
        :param str _: required.
        :param str _: required.

        - JWT required.
        - **Admin only.**
        - Header: `\"Authorization\": \"Bearer {access_token}\"`
        """
        current_user = get_jwt_identity()
        role = current_user['role']
        checkAdmin(role)
        
        try:
            args = parser_info.parse_args()
            username = args['username']
            result = users.UserModel.query.filter_by(username=username).first()

            if args["first_name"]:
                result.first_name = args["first_name"]
        
            if args["last_name"]:
                result.last_name = args["last_name"]
        
            if args["email"]:
                result.email = args["email"]

            if args["role"]: 
                result.role = args["role"]

            db.session.commit()

            return {
                'username': result.username,
                'first_name': result.first_name,
                'last_name': result.last_name,
                'email': result.email,
                'role': result.role    
                }, 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500

api.add_resource(Register, '/users/register')
api.add_resource(Profile, '/users/me')
api.add_resource(AllUsers, '/users/all')
api.add_resource(ChangeUserDetail, '/users/update')
