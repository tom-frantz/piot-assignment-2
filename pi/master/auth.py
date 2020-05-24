from flask_restful import abort
from master.models import users
from passlib.handlers.pbkdf2 import pbkdf2_sha256 as sha256
from sqlalchemy.exc import SQLAlchemyError


def check_user_exists(user):
    try:
        result = users.UserModel.query.filter_by(username=user).first()
        if result is None:
            return 401, 'User doesn\'t exist.'
            # abort(401, message='User doesn\'t exist.')
        else:
            return 200, result.password
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return 500, error


def verify_password(password, hashed_password):
    try:
        if not sha256.verify(password, hashed_password):
            return False, 'The password is wrong.'
        else:
            return True, None
    # when password is not a valid sha256 hashed value
    except ValueError:
        return False, 'The password in database is not in the right format.'
