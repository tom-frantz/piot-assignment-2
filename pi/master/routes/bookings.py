from flask_restful import reqparse, abort, Resource
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from master import app, api, db
from sqlalchemy.exc import SQLAlchemyError
from master.models import bookings, cars, users

parser_new = reqparse.RequestParser()
parser_new.add_argument('car_number', required=True)

parser_cancel = reqparse.RequestParser()
parser_cancel.add_argument('booking_id', required=True)


class MyBookedCars(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()

        try:
            result = bookings.BookingModel.query.filter_by(
                username=current_user).all()
            booked_cars = list(map(lambda item: item.car_number, result))
            return booked_cars, 200
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig']).strip("\\")
            return {'message': error}, 500


class NewBooking(Resource):
    @jwt_required
    def post(self):
        current_user = get_jwt_identity()

        args = parser_new.parse_args()
        car_number = args['car_number']

        new_booking = bookings.BookingModel(
            car_number=car_number,
            username=current_user
        )

        try:
            new_booking.save_to_db()
            return {
                'message': "Your booking {} has been successfully created.".format(booking_id)
            }
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class CancelBooking(Resource):
    @jwt_required
    def put(self):
        args = parser_new.parse_args()
        current_booking = args['booking_id']

        try:
            result = bookings.BookingModel.query.filter_by(
                booking_id=current_booking).first()
            result.active = False
            db.session.commit()
            return ({
                'message': "Your booking {} has been canceled.".format(current_booking)
            }, 200)
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig']).strip("\\")
            return {'message': error}, 500


api.add_resource(MyBookedCars, '/bookings/me')
api.add_resource(NewBooking, '/bookings/new')
api.add_resource(CancelBooking, '/bookings/cancel')
