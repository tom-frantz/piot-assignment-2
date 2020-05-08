from flask_restful import reqparse, abort, Resource
from flask_jwt_extended import jwt_required
from master import app, api
from sqlalchemy.exc import SQLAlchemyError
from master.models import cars

# import sys

parser_new = reqparse.RequestParser()
parser_new.add_argument('car_number', required=True)
parser_new.add_argument('seats', required=True)
parser_new.add_argument('lock_status')
parser_new.add_argument('available')

# TODO: admin only


class NewCar(Resource):
    @jwt_required
    def post(self):
        args = parser_new.parse_args()
        car_number = args['car_number']
        seats = args['seats']

        # optional request arguments
        lock_status = True
        available = True

        if args['lock_status'] is not None:
            lock_status = args['lock_status']

        if args['available'] is not None:
            lock_status = args['available']

        new_car = cars.CarModel(
            car_number=car_number,
            seats=seats,
            lock_status=lock_status,
            available=available
        )

        try:
            new_car.save_to_db()
            return ({'car_number': car_number,
                     'seats': seats,
                     'lock_status': lock_status,
                     'available': available
                     })
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500

        return ({"message": "API for adding a new car."})


class CarDetail(Resource):
    @jwt_required
    def get(self, car_number):
        try:
            result = cars.CarModel.query.filter_by(
                car_number=car_number).first()
            return ({"car_number": result.car_number,
                     "seats": result.seats,
                     "lock_status": result.lock_status,
                     "available": result.available}, 200)

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class AvailableCars(Resource):
    @jwt_required
    def get(self):
        try:
            result = cars.CarModel.query.filter_by(available=True).all()

            available_cars = list(map(lambda item: {
                "car_number": item.car_number,
                "seats": item.seats}, result))
            return available_cars, 200

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class SearchCarBySeats(Resource):
    @jwt_required
    def get(self, seats):

        try:
            result = cars.CarModel.query.filter_by(seats=seats).all()
            filtered_cars = list(map(lambda item: {
                "car_number": item.car_number,
                "seats": item.seats,
                "lock_status": item.lock_status,
                "avaialble": item.available}, result))
            return filtered_cars, 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


api.add_resource(NewCar, '/cars/new')
api.add_resource(CarDetail, '/cars/detail/<string:car_number>')
api.add_resource(AvailableCars, '/cars/available')
api.add_resource(SearchCarBySeats, '/cars/seats/<int:seats>')
