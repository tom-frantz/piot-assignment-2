import socketio


def login(socket):
    socket.emit(
        "login", {"username": "user", "password": "password"}, callback=login_callback,
    )


def login_callback(res):
    pass


def refresh(socket):
    socket.emit(
        "refresh",
        {
            "refresh_token": 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkwODEzMzIsIm5iZiI6MTU4OTA4MTMzMiwianRpIjoiNWFiYzc5ODQtMTMyYi00MWE4LWFmODAtYjIyMGQ1NzI1ZWY2IiwiZXhwIjoxNTkxNjczMzMyLCJpZGVudGl0eSI6InVzZXIiLCJ0eXBlIjoicmVmcmVzaCJ9.If9yQtW_ptRk9vJ2AsmnZ-xqzx1zo1yA_O6LykrObRU'
        },
        callback=refresh_callback,
    )


def refresh_callback(res):
    pass


def update_loc(socket):
    socket.emit("location_update")


def update_loc_callback(res):
    pass


if __name__ == '__main__':
    s = socketio.Client()
    print("Connecting")
    s.connect("http://127.0.0.1:5000")
    refresh(s)
    print("Done")
# s.disconnect()
