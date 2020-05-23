from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from master import socketio
from master.models import bookings, cars
from master.car_operation import user_unlock_car, user_return_car
from master.sockets.utils import success_response, error_response

debug = True


@socketio.on("unlock_car")
def unlock_car(data):
    #    booking_number = data['booking_number']
    car_number = data['car_number']
    try:
        result = cars.CarModel.query.filter_by(
            car_number=car_number, lock_status=True).first()
        if result is False:
            return 401, 'this car status is not locking.'
        else:
            return 100, 'this car unlock successfully'
    except Exception as e:
        error = str(e.__dict__['orig'])
        return 500, error


@socketio.on("return_car")
def return_car(data):
    try:
        result = True
        if result is False:
            return 'this car status is not renting.'
        else:
            return 'this car return successfully'
    except Exception as e:
        error = str(e.__dict__['orig'])
        return error
