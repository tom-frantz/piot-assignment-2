from flask_restful import reqparse, abort, Resource, inputs
from flask_jwt_extended import (
    jwt_required,
    get_jwt_identity,
)
from master import app, api, db
from sqlalchemy.exc import SQLAlchemyError
from master.models import bookings, cars
from datetime import date, datetime, timedelta

parser_new = reqparse.RequestParser(bundle_errors=True)
parser_new.add_argument(
    'car_number', type=inputs.regex('^[A-Za-z0-9]{1,6}$'), required=True
)

# "2013-01-01T06:00/2013-01-01T12:00" -> datetime(2013, 1, 1, 6), datetime(2013, 1, 1, 12)
# "2013-01-01/2013-01-01" -> date(2013, 1, 1), date(2013, 1, 1)
# A tuple of depature and return time in iso8601 format
parser_new.add_argument('booking_period', type=inputs.iso8601interval)


def validate_booking_period(car_number, departure_time, return_time):
    try:
        result = bookings.BookingModel.query.filter_by(
            car_number=car_number).all()
        if result is None:
            pass
        else:
            for i in result:
                if departure_time.date() < datetime.utcnow().date():
                    abort(403, message='You can\'t make a booking on past days.')
                elif (
                    i.departure_time.date()
                    <= departure_time.date()
                    <= i.return_time.date()
                    or i.departure_time.date()
                    <= return_time.date()
                    <= i.return_time.date()
                    or (i.departure_time.date() <= departure_time.date()
                        and i.return_time.date() >= return_time.date())
                ):
                    abort(
                        403,
                        message='Car {} is not available on selected days.'.format(
                            car_number
                        ),
                    )
                else:
                    pass
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        abort(500, message=error)


class MyBookedCars(Resource):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()

        try:
            result = bookings.BookingModel.query.filter_by(
                username=current_user).all()
            booked_cars = list(
                map(
                    lambda item: {
                        'booking_id': item.booking_id,
                        'car_number': item.car_number,
                        'departure_time': item.departure_time.isoformat(),
                        'return_time': item.return_time.isoformat(),
                        'created_at': item.created_at.isoformat(),
                    },
                    result,
                )
            )
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
        car_number = car_number.upper()
        booking_period = args['booking_period']
        departure_time = booking_period[0]
        return_time = booking_period[1]

        validate_booking_period(car_number, departure_time, return_time)

        new_booking = bookings.BookingModel(
            car_number=car_number,
            username=current_user,
            departure_time=departure_time,
            return_time=return_time,
        )

        try:

            new_booking.save_to_db()
            return {
                'message': "Your booking (id: {}) for car {} has been successfully created.".format(
                    new_booking.booking_id, car_number
                )
            }
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


class CancelBooking(Resource):
    @jwt_required
    def delete(self, booking_id):

        try:
            result_booking = bookings.BookingModel.query.filter_by(
                booking_id=booking_id
            ).delete()

            db.session.commit()
            return (
                {
                    'message': "Your booking {} has been canceled.".format(
                        booking_id
                    )
                },
                200,
            )
        except SQLAlchemyError as e:
            error = str(e.__dict__['orig'])
            return {'message': error}, 500


api.add_resource(MyBookedCars, '/bookings/me')
api.add_resource(NewBooking, '/bookings/new')
api.add_resource(CancelBooking, '/bookings/cancel/<int:booking_id>')
