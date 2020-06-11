"""
RESTful API Routes: `/access_token/{endpoint}`
"""

from flask_restful import reqparse, abort, Resource, inputs
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
)
from master.auth import check_user_exists, verify_password
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.exc import SQLAlchemyError
from master import app, api, db
from master.models import users


parser_get_tokens = reqparse.RequestParser(bundle_errors=True)
parser_get_tokens.add_argument(
    'username', type=inputs.regex('^[A-Za-z0-9-_]{3,15}$'), required=True
)
parser_get_tokens.add_argument(
    'password', type=inputs.regex('^[A-Za-z0-9-_]{8,30}$'), required=True
)

parser_change_password = reqparse.RequestParser(bundle_errors=True)
parser_change_password.add_argument(
    'old_password', type=inputs.regex('^[A-Za-z0-9-_]{8,30}$'), required=True
)
parser_change_password.add_argument(
    'new_password', type=inputs.regex('^[A-Za-z0-9-_]{8,30}$'), required=True
)


def check_user(current_user, password):
    """
    A help method to verify user password in database.
    """
    code, result = check_user_exists(current_user)  # return status code + password
    if code != 200:
        abort(code, message=result["message"])
    stored_password = result["password"]
    ok, msg = verify_password(password, stored_password)
    if not ok:
        abort(401, message=msg)
    return result["role"]


class AccessToken(Resource):
    """
    User login
    """

    def post(self):
        """
        :param str username: required.
        :param str password: required.
        """
        args = parser_get_tokens.parse_args()
        username = args['username']
        password = args['password']

        role = check_user(username, password)

        user_identity = {'username': username, 'role': role}
        access_token = create_access_token(identity=user_identity)
        refresh_token = create_refresh_token(identity=user_identity)

        return (
            {
                'username': username,
                'access_token': access_token,
                'refresh_token': refresh_token,
            },
            201,
        )


class TokenRefresh(Resource):
    """
    Re-generate access token based on refresh token.
    """

    @jwt_refresh_token_required
    def post(self):
        """
        - JWT refresh token required.
        - Header: `\"Authorization\": \"Bearer {refresh_token}\"`
        """
        current_user = get_jwt_identity()  # extract identity from refresh token
        username = current_user['username']
        code, res = check_user_exists(username)

        if code != 200:
            abort(code, message=res)

        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 201


class ChangePassword(Resource):
    """
    Change password.
    """

    @jwt_required
    def post(self):
        """
        :param str old_password: required.
        :param str new_password: required.

        - JWT required.
        - Header: `\"Authorization\": \"Bearer {access_token}\"`
        """
        current_user = get_jwt_identity()
        username = current_user['username']
        args = parser_change_password.parse_args()
        old_password = args['old_password']
        new_password = args['new_password']

        result = check_user_exists(username)  # password string
        stored_password = result.password
        verify_password(old_password, stored_password)

        try:
            # user = users.UserModel.query.filter_by(username=current_user).first()
            result.password = sha256.hash(new_password)
            db.session.commit()
            identity = {'username': result.username, 'role': result.role}
            access_token = create_access_token(identity=identity)
            refresh_token = create_refresh_token(identity=identity)
            return {'access_token': access_token, "refresh_token": refresh_token}, 201
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"Error": error}, 500


api.add_resource(AccessToken, '/access_token/new')
api.add_resource(TokenRefresh, '/access_token/refresh')
