from flask_restful import reqparse, abort, Resource, inputs, request
from flask_jwt_extended import jwt_required
from master import app, api, db
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import and_
from master.models import cars, bookings
import master.validation as validate
import re
import simplejson as json

debug = True

# request parser: adding a new car
parser_new = reqparse.RequestParser(bundle_errors=True)
parser_new.add_argument(
    'car_number', type=inputs.regex('^[A-Za-z0-9]{1,6}$'), required=True
)
parser_new.add_argument('make', type=validate.string_30, required=True)
parser_new.add_argument('body_type', type=validate.string_30, required=True)
parser_new.add_argument('colour', type=validate.string_30, required=True)
parser_new.add_argument('seats', type=inputs.int_range(1, 12), required=True)
parser_new.add_argument('cost_per_hour', type=validate.price, required=True)
parser_new.add_argument('latitude', type= validate.latitude_decimal)
parser_new.add_argument('longitude', type = validate.longitude_decimal)
# !!ATTENTION!!
# Req body must input string 'true' or 'false' (case sensitive) as boolean value
parser_new.add_argument('lock_status', type=inputs.boolean)

# request parser: available cars
parser_available = reqparse.RequestParser()
# "2013-01-01T06:00/2013-01-01T12:00" -> datetime(2013, 1, 1, 6), datetime(2013, 1, 1, 12)
# "2013-01-01/2013-01-01" -> date(2013, 1, 1), date(2013, 1, 1)
# A tuple of depature and return time in iso8601 format
parser_available.add_argument('time_range', type=inputs.iso8601interval)

class NewCar(Resource):
    @jwt_required
    def post(self):
        args = parser_new.parse_args()
        car_number = args['car_number']
        car_number = car_number.upper()

        make = args['make']
        body_type = args['body_type']
        colour = args['colour']
        seats = args['seats']
        cost_per_hour = args['cost_per_hour']

        # optional request arguments by default
        latitude = -37.804663448
        longitude = 144.957996168
        lock_status = True

        if args['latitude'] is not None:
            latitude = args['latitude']

        if args['longitude'] is not None:
            longitude = args['longitude']

        if args['lock_status'] is not None:
            lock_status = args['lock_status']

        new_car = cars.CarModel(
            car_number=car_number,
            make=make,
            body_type=body_type,
            colour=colour,
            seats=seats,
            cost_per_hour=cost_per_hour,
            latitude=latitude,
            longitude=longitude,
            lock_status=lock_status,
        )

        try:
            new_car.save_to_db()
            return ({
                'car_number': car_number,
                'make': make,
                'body_type': body_type,
                'colour': colour,
                'seats': seats,
                'cost_per_hour': cost_per_hour,
                'latitude': latitude,
                'longitude': longitude,
                'lock_status': lock_status,
            }, 201)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class CarDetail(Resource):
    @jwt_required
    def get(self, car_number):
        try:
            inputs.regex('^[A-Za-z0-9]{1,6}$')(car_number)

            car_number = car_number.upper()
            result = cars.CarModel.query.filter_by(
                car_number=car_number).first()
            return (
                {
                    "car_number": result.car_number,
                    "make": result.make,
                    "body_type": result.body_type,
                    "colour": result.colour,
                    "seats": result.seats,
                    "latitude": json.dumps(result.latitude, use_decimal=True),
                    "longitude": json.dumps(result.longitude, use_decimal=True),
                    "cost_per_hour": json.dumps(result.cost_per_hour, use_decimal=True),
                    "lock_status": result.lock_status,
                },
                200,
            )

        except ValueError as ve:
            return {'message': str(ve)}, 403
        except SQLAlchemyError as se:
            error = str(se.__dict__['orig'])
            return {'message': error}, 500


class AvailableCars(Resource):
    @jwt_required
    def get(self):
        args = parser_available.parse_args()

        time_range = args['time_range']
        start_time = time_range[0]
        end_time = time_range[1]

        try:
            car_model = cars.CarModel
            booking_model = bookings.BookingModel
            booked_cars = db.session.query(car_model.car_number).join(booking_model).filter(and_(
                booking_model.departure_time <= end_time, booking_model.return_time >= start_time)).subquery()
            filtered_result = db.session.query(car_model).filter(
                car_model.car_number.notin_(booked_cars)).all()
            available_cars = list(
                map(lambda item: {
                    "car_number": item.car_number,
                    "make": item.make,
                    "body_type": item.body_type,
                    "colour": item.colour,
                    "seats": item.seats,
                    "latitude": json.dumps(item.latitude, use_decimal=True),
                    "longitude": json.dumps(item.longitude, use_decimal=True),
                    "cost_per_hour": json.dumps(item.cost_per_hour, use_decimal=True),
                    "lock_status": item.lock_status,
                }, filtered_result)
            )
            return available_cars, 200

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class SearchCars(Resource):
    @jwt_required
    def get(self):
        # TODO: validation of request args

        try:
            result = cars.CarModel.query.filter_by(**request.args).all()
            filtered_cars = list(
                map(
                    lambda item: {
                        "car_number": item.car_number,
                        'make': item.make,
                        'body_type': item.body_type,
                        "seats": item.seats,
                        "colour": item.colour,
                        "latitude": json.dumps(item.latitude, use_decimal=True),
                        "longitude": json.dumps(item.longitude, use_decimal=True),
                        "cost_per_hour": json.dumps(item.cost_per_hour, use_decimal=True),
                        "lock_status": item.lock_status,
                    },
                    result,
                )
            )
            return filtered_cars, 200
            # return {'get': args['make']}, 200
        except ValueError as ve:
            return {'message': "Car seats should be in range 1-12 inclusive."}, 403
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class AllCars(Resource):
    @jwt_required
    def get(self):
        try:
            all_cars = cars.CarModel.query.all()

            car_list = []
            for item in all_cars:
                car_item = {
                    'car_number': item.car_number,
                    'make': item.make,
                    'body_type': item.body_type,
                    "seats": item.seats,
                    "colour": item.colour,
                    "latitude": json.dumps(item.latitude, use_decimal=True),
                    "longitude": json.dumps(item.longitude, use_decimal=True),
                    "cost_per_hour": json.dumps(item.cost_per_hour, use_decimal=True),
                    "lock_status": item.lock_status,
                    "bookings": []
                }
                all_bookings = bookings.BookingModel.query.filter_by(
                    car_number=item.car_number).all()
                if len(all_bookings) > 0:
                    booking_list = list(map(lambda i: {
                        'booking_id': i.booking_id,
                        'username': i.username,
                        'departure_time': i.departure_time.isoformat(),
                        'return_time': i.return_time.isoformat(),
                        'created_at': i.created_at.isoformat()
                    }, all_bookings))
                    car_item['bookings'] = booking_list
                car_list.append(car_item)

            return car_list, 200

        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500

class ReturnCars(Resource):
    @jwt_required
    def post(self):
        return {'message': "3333333."}, 200

    @jwt_required
    def get(self):
        # TODO: validation of request args
        if debug:
            return {'message': "Car seats should be in range 1-12 inclusive."}, 200
        try:
            result = cars.CarModel.query.filter_by(**request.args).all()
            filtered_cars = list(
                map(
                    lambda item: {
                        "car_number": item.car_number,
                        'make': item.make,
                        'body_type': item.body_type,
                        "seats": item.seats,
                        "colour": item.colour,
                        "latitude": json.dumps(item.latitude, use_decimal=True),
                        "longitude": json.dumps(item.longitude, use_decimal=True),
                        "cost_per_hour": json.dumps(item.cost_per_hour, use_decimal=True),
                        "lock_status": item.lock_status,
                    },
                    result,
                )
            )
            return filtered_cars, 200
            # return {'get': args['make']}, 200
        except ValueError as ve:
            return {'message': "Car seats should be in range 1-12 inclusive."}, 403
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500

class UnlockCars(Resource):
    @jwt_required
    def post(self):
        print("3333333333")
        return {'message': "222222222."}, 200

    @jwt_required
    def get(self):
        # TODO: validation of request args
        print("111111111111")

        if debug:
            print("UnlockCarsUnlockCarsUnlockCarsUnlockCarsUnlockCarsUnlockCars")
            return {'message': "Car seats should be in range 1-12 inclusive."}, 200
        try:
            result = cars.CarModel.query.filter_by(**request.args).all()
            filtered_cars = list(
                map(
                    lambda item: {
                        "car_number": item.car_number,
                        'make': item.make,
                        'body_type': item.body_type,
                        "seats": item.seats,
                        "colour": item.colour,
                        "latitude": json.dumps(item.latitude, use_decimal=True),
                        "longitude": json.dumps(item.longitude, use_decimal=True),
                        "cost_per_hour": json.dumps(item.cost_per_hour, use_decimal=True),
                        "lock_status": item.lock_status,
                    },
                    result,
                )
            )
            return filtered_cars, 200
            # return {'get': args['make']}, 200
        except ValueError as ve:
            return {'message': "Car seats should be in range 1-12 inclusive."}, 403
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500

api.add_resource(NewCar, '/cars/new')
api.add_resource(CarDetail, '/cars/detail/<string:car_number>')
api.add_resource(AvailableCars, '/cars/available')
api.add_resource(SearchCars, '/cars/search')
api.add_resource(AllCars, '/cars/all')
# return car 
api.add_resource(ReturnCars, '/cars/return')
# unlock car
api.add_resource(UnlockCars, '/cars/unlock')