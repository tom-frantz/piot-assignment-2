from flask_restful import Resource
from master import app, api

class Home(Resource):
    def get(self):
        return {"message": "This is CarShare API."}


api.add_resource(Home, '/')
