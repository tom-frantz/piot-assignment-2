"""
Queue message and callback operations.
"""

import socketio
import time
import traceback
import urllib
import sys

# sio = socketio.Client(engineio_logger=Fasle)
sio = socketio.Client()
start_timer = None


class GlobalConf(object):
    recv_queue = None
    access_token = None
    refresh_token = None
    """docstring for GlobalConf"""

    def __init__(self, arg):
        # super(GlobalConf, self).__init__()
        self.arg = ""


Global_url = "http://127.0.0.1:5000/{}"
Global_return_queue = None


def op_unlock_car(sio, data):
    """
    Unlock car message.
    """
    try:
        data["access_token"] = GlobalConf.access_token
        data["refrsh_token"] = GlobalConf.refresh_token
        uri = "unlock_car"
        if GlobalConf.access_token is None:
            print("Please login first, system is to shut down.")
            sys.exit(0)
        else:
            res = sio.emit(uri, data, callback=op_unlock_car_callback(data))
        print(data)
    except Exception as err:
        traceback.print_exc()
        jdata = {"error": str(err)}
        GlobalConf.recv_queue.put(jdata)


def op_unlock_car_callback(data):
    print("op_unlock_car_callback in process")
    GlobalConf.recv_queue.put(data)


def op_return_car(sio, data):
    """
    Return car message.
    """
    try:
        data["access_token"] = GlobalConf.access_token
        data["refrsh_token"] = GlobalConf.refresh_token
        uri = "return_car"
        if GlobalConf.access_token is None:
            print("Please login first, system is to shut down.")
            sys.exit(0)
        else:
            res = sio.emit(uri, data, callback=op_return_car_callback(data))
    except Exception as err:
        traceback.print_exc()
        jdata = {"error": str(err)}
        GlobalConf.recv_queue.put(jdata)


def op_return_car_callback(data):
    print("op_return_car_callback in process.")
    GlobalConf.recv_queue.put(data)


def refresh(socket):
    socket.emit(
        "refresh",
        {
            "refresh_token": 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpYXQiOjE1ODkwODEzMzIsIm5iZiI6MTU4OTA4MTMzMiwianRpIjoiNWFiYzc5ODQtMTMyYi00MWE4LWFmODAtYjIyMGQ1NzI1ZWY2IiwiZXhwIjoxNTkxNjczMzMyLCJpZGVudGl0eSI6InVzZXIiLCJ0eXBlIjoicmVmcmVzaCJ9.If9yQtW_ptRk9vJ2AsmnZ-xqzx1zo1yA_O6LykrObRU'
        },
        callback=refresh_callback,
    )


def op_login(sio, data):
    """
    Return data formate:
    
    `cmd,data = "login", {"username": "user", "password": "password"}`
    """
    try:
        res = sio.emit("login", data, callback=op_login_callback,)
    except Exception as err:
        jdata = {"error": str(err)}
        GlobalConf.recv_queue.put(jdata)


def op_login_callback(data):
    # {'success': True, 'username': '1', 'access_token': 'access_token', 'refresh_token': 'refresh_token'}
    GlobalConf.access_token = data.get("access_token")
    GlobalConf.refresh_token = data.get("refresh_token")
    GlobalConf.recv_queue.put(data)


def client_start(send_queue, recv_queue):
    """
    Client menu command patterns.
    """
    sio.connect('http://localhost:5000')
    # sio.wait()
    GlobalConf.recv_queue = recv_queue
    while 1:
        data = send_queue.get()
        cmd = data.get("cmd")
        if cmd == "login":
            op_login(sio, data)
        elif cmd == "unlock_car":
            op_unlock_car(sio, data)
        elif cmd == "return_car":
            op_return_car(sio, data)


@sio.event
def connect():
    print(' ')
    print('connection established')
    print(' ')


if __name__ == '__main__':
    main()
