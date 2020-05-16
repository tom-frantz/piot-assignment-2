from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from master import socketio
from master.car_operation import user_unlock_car, user_return_car
from master.sockets.utils import success_response, error_response
debug = True

@socketio.on("unlock_car")
def unlock_car(data):
    if debug:
        # print("0000000000000")
        return success_response(
        username="username", access_token="access_token", refresh_token="refresh_token",
    )
    ok, res = user_unlock_car(username)  # TODO
    return success_response(
        unlock_car_result=ok, unlock_car_response=res
    )

@socketio.on("return_car")
def return_car(data):
    if debug:
        return success_response(
        username=username, access_token="access_token", refresh_token="refresh_token",
    )
    ok, res =user_return_car(username)
    return success_response(
        return_car_result=ok, return_car_response=res
    )