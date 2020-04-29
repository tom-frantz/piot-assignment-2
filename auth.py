from flask_restful import reqparse, abort, Resource

parser = reqparse.RequestParser()
parser.add_argument('username')
username = ['a', 'b', 'c']


def auth_failure(user):
    if user not in username:
        abort(401, message='Auth failed.')


class Auth(Resource):
    def post(self):
        args = parser.parse_args()
        new_user = args['username']
        auth_failure(new_user)
        return {
            'username': new_user,
            'encrypt_key': 'key_value'}, 201
