from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from master import socketio
from master.models import users
from master.auth import verify_password, check_user_exists
from master.sockets.utils import success_response, error_response


@socketio.on("login")
def login(data):
    """
    recive a login reuqest from AP

    :param String username: required.
    :param String password: required.

    """
    username = data["username"]
    password = data["password"]

    ok, res = check_user_exists(username)  # TODO
    if ok != 200:
        return error_response(res)

    hashed_password = res["password"]
    role = res["role"]

    ok, msg = verify_password(password, hashed_password)
    if not ok:
        return error_response(msg)

    identity = {"username": username, "role": role}
    access_token = create_access_token(identity=identity)
    refresh_token = create_refresh_token(identity=identity)
    return success_response(
        username=username, access_token=access_token, refresh_token=refresh_token,
    )


@socketio.on("bluetooth_login")
def bluetooth_login(data):
    """
    recive a bluetooth login reuqest from AP

    :param String mac_address: required.   
    """
    print("recive socket")
    engineer_mac_addr = data["engineer_mac"]

    result = users.UserModel.query.filter_by(mac_address=engineer_mac_addr).first()
    user_name = result.username
    print(user_name, result.mac_address)
    if result is None:
        return error_response("engineer login fail")
    else:
        identity = {"username": user_name, "role": "engineer"}
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)
    return success_response(
        username=user_name, access_token=access_token, refresh_token=refresh_token,
    )


@socketio.on("refresh")
def refresh(data):
    try:
        token = decode_token(data["refresh_token"])
        if token["type"] != refresh:
            return error_response("The token was invalid")

        check_user_exists(token["identity"])
        access_token = create_access_token(identity=token["identity"])

        return success_response(access_token=access_token)
    except Exception as e:
        return error_response("The token was invalid")
