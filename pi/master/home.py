from flask_restful import Resource, Api
from master import app


class Home(Resource):
    def get(self):
        return {'message': 'CarShare App API'}


api = Api(app)

api.add_resource(Home, '/')
