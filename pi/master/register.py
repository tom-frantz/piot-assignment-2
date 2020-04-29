from flask_restful import reqparse, abort, Resource

parser = reqparse.RequestParser()
parser.add_argument('username')
username = ['a', 'b', 'c']


def user_already_exists(user):
    if user in username:
        abort(403, message='User already exists.')


class Register(Resource):
    def post(self):
        args = parser.parse_args()
        new_user = args['username']
        user_already_exists(new_user)
        return {'username': new_user, 'encrypt_key': 'key_value'}, 201
