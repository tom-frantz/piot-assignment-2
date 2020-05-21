from flask_jwt_extended import create_access_token, create_refresh_token, decode_token
from master import socketio
from master.auth import verify_password, check_user_exists
from master.sockets.utils import success_response, error_response
from passlib.hash import pbkdf2_sha256 as sha256


@socketio.on("login")
def login(data):
    username = data["username"]
    password = data["password"]
    ok, res = check_user_exists(username)  # TODO
    if ok != 200:
        return error_response(res)

    hashed_password = sha256.hash(str(res))

    ok, msg = verify_password(password, hashed_password)
    if not ok:
        return error_response(msg)

    access_token = create_access_token(identity=username)
    refresh_token = create_refresh_token(identity=username)
    return success_response(
        username=username, access_token=access_token, refresh_token=refresh_token,
    )


@socketio.on("refresh")
def refresh(data):
    try:
        token = decode_token(data["refresh_token"])
        if token["type"] != "refresh":
            return error_response("The token was invalid")

        check_user_exists(token["identity"])
        access_token = create_access_token(identity=token["identity"])

        return success_response(access_token=access_token)
    except Exception as e:
        return error_response("The token was invalid")
