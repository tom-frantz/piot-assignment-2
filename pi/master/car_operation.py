from flask_restful import abort
from master.models import users
from passlib.handlers.pbkdf2 import pbkdf2_sha256 as sha256
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from master import socketio
from master.auth import verify_password, check_user_exists
from master.sockets.utils import success_response, error_response


@socketio.on("refresh")
def refresh(data):
    try:
        token = decode_token(data["refresh_token"])
        if token["type"] != "refresh":
            return error_response("The token was invalid")

        check_user_exists(token["identity"])
        access_token = create_access_token(identity=token["identity"])

        return success_response(access_token=access_token)
    except Exception as e:
        return error_response("The token was invalid")


def user_unlock_car():

    # sql =
    return "ok", "res"


def user_return_car():
    # sql =
    return "ok", "res"


def check_user_exists(user):
    try:
        result = users.UserModel.query.filter_by(username=user).first()
        if result is None:
            return 401, 'User doesn\'t exist.'
            # abort(401, message='User doesn\'t exist.')
        else:
            return 200, result
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return 500, error


def verify_password(password, hashed_password):
    try:
        if not sha256.verify(password, hashed_password):
            return False, 'The password is wrong.'
    # when password is not a valid sha256 hashed value
    except ValueError:
        return False, 'The password in database is not in the right format.'
    finally:
        return True, None
