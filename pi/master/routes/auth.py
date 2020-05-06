from flask_restful import reqparse, abort, Resource
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
)
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.exc import SQLAlchemyError
from master import app, api, db
from master.models import users


parser_get_tokens = reqparse.RequestParser(bundle_errors=True)
parser_get_tokens.add_argument('username', required=True)
parser_get_tokens.add_argument('password', required=True)

parser_change_password = reqparse.RequestParser(bundle_errors=True)
parser_change_password.add_argument('old_password', required=True)
parser_change_password.add_argument('new_password', required=True)


def check_user_exists(user):
    try:
        result = users.UserModel.query.filter_by(username=user).first()
        if result is None:
            abort(401, message='User doesn\'t exist.')
        else:
            return result
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return {"Error": error}, 500


def verify_password(password, hashed_password):
    try:
        if not sha256.verify(password, hashed_password):
            abort(401, message='The password is wrong.')
    # when password is not a valid sha256 hashed value
    except ValueError:
        abort(401, message='The password in database is not in the right format.')


class AccessToken(Resource):
    def post(self):
        args = parser_get_tokens.parse_args()
        username = args['username']
        password = args['password']
        hashed_password = check_user_exists(username).password
        verify_password(password, hashed_password)

        access_token = create_access_token(identity=username)
        refresh_token = create_refresh_token(identity=username)
        return (
            {
                'username': username,
                'access_token': access_token,
                'refresh_token': refresh_token,
            },
            201,
        )


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()  # extract identity from refresh token
        check_user_exists(current_user)
        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 201


class ChangePassword(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        args = parser_change_password.parse_args()
        old_password = args['old_password']
        new_password = args['new_password']

        result = check_user_exists(current_user)
        stored_password = result.password
        verify_password(old_password, stored_password)

        try:
            # user = users.UserModel.query.filter_by(username=current_user).first()
            result.password = sha256.hash(new_password)
            db.session.commit()
            access_token = create_access_token(identity=result.username)
            refresh_token = create_refresh_token(identity=result.username)
            return {'access_token': access_token, "refresh_token": refresh_token}, 201
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {"Error": error}, 500


api.add_resource(AccessToken, '/auth/new')
api.add_resource(TokenRefresh, '/auth/refresh')
api.add_resource(ChangePassword, '/auth/password')
