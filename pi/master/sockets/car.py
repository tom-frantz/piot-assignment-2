from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from master import socketio
from master.models import bookings, cars
from master.car_operation import user_unlock_car, user_return_car
from master.sockets.utils import success_response, error_response
from master import db


@socketio.on("unlock_car")
def unlock_car(data):
    car_number = data["car_number"]
    try:
        result = cars.CarModel.query.filter_by(car_number=car_number).first()
        result.lock_status = True
        db.session.commit()
        if result is None:
            return 401, 'result has no return value'
        else:
            return 100, 'result has value'
    except Exception as e:
        error = str(e.__dict__['orig'])
        return 500, error


@socketio.on("return_car")
def return_car(data):
    car_number = data["return_car_number"]
    try:
        result = cars.CarModel.query.filter_by(car_number=car_number).first()
        result.lock_status = False
        db.session.commit()
        if result is False:
            return 'this car status is not renting.'
        else:
            return 'this car return successfully'
    except Exception as e:
        error = str(e.__dict__['orig'])
        return error
