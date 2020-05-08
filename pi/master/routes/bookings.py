from flask_restful import reqparse, abort, Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from master import app, api, db
from sqlalchemy.exc import SQLAlchemyError
from master.models import bookings, cars

parser_new = reqparse.RequestParser()
parser_new.add_argument('car_number', required=True)

parser_cancel = reqparse.RequestParser()
parser_cancel.add_argument('booking_id', required=True)

def check_and_book(car_number):
    try:
        result = cars.CarModel.query.filter_by(car_number=car_number).first()
        if not result.available:
            abort(403, message='The car has already been booked.')
        else:
            result.available=False
            db.session.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        return {'message': error}, 500

class MyBookedCars(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()

        try:
            result = bookings.BookingModel.query.filter_by(
                username=current_user).all()
            booked_cars = list(map(lambda item: {
                'booking_id': item.booking_id,
                'car_number': item.car_number,
                'created_at': item.created_at.isoformat()}, result))
            return booked_cars, 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class NewBooking(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()

        args = parser_new.parse_args()
        car_number = args['car_number']

        check_and_book(car_number)

        new_booking = bookings.BookingModel(
            car_number=car_number,
            username=current_user
        )

        try:

            new_booking.save_to_db()
            return {
                'message': "Your booking for car {} has been successfully created.".format(car_number)
            }
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class CancelBooking(Resource):
    @jwt_required
    def put(self):
        args = parser_cancel.parse_args()
        current_booking = args['booking_id']

        try:
            result_booking = bookings.BookingModel.query.filter_by(
                booking_id=current_booking).first()
            result_booking.active = False

            result_car = cars.CarModel.query.filter_by(car_number= result_booking.car_number).first()
            result_car.available = True

            db.session.commit()
            return ({
                'message': "Your booking {} has been canceled.".format(current_booking)
            }, 200)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


api.add_resource(MyBookedCars, '/bookings/me')
api.add_resource(NewBooking, '/bookings/new')
api.add_resource(CancelBooking, '/bookings/cancel')
