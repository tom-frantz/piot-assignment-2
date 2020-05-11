from flask_restful import reqparse, Resource, abort
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
from master import api, db

parser_get_tokens = reqparse.RequestParser(bundle_errors=True)
parser_get_tokens.add_argument('username', required=True)
parser_get_tokens.add_argument('password', required=True)

parser_change_password = reqparse.RequestParser(bundle_errors=True)
parser_change_password.add_argument('old_password', required=True)
parser_change_password.add_argument('new_password', required=True)


def check_user(current_user, password):
    code, result = check_user_exists(current_user)
    if code != 200:
        abort(code, message=result)
    stored_password = result.password
    ok, msg = verify_password(password, stored_password)
    if not ok:
        abort(401, message=msg)
    return result


class AccessToken(Resource):
    def post(self):
        args = parser_get_tokens.parse_args()
        username = args['username']
        password = args['password']

        check_user(username, password)

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
        code, res = check_user_exists(current_user)

        if code != 200:
            abort(code, message=res)

        access_token = create_access_token(identity=current_user)
        return {'access_token': access_token}, 201


class ChangePassword(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        args = parser_change_password.parse_args()
        old_password = args['old_password']
        new_password = args['new_password']

        result = self.check_user(current_user, old_password)

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
