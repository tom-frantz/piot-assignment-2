import socketio
import time
import traceback
import urllib

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

# @sio.event
# def message(data):
#     print('I received a message!')

# @sio.on('success')
# def on_message(data):
#     print(data)
#     print('I received a message!')


# @sio.event
# def connect():
#     print("I'm connected!")

# @sio.event
# def connect_error():
#     print("The connection failed!")

# @sio.event
# def disconnect():
#     print("I'm disconnected!")

def op_unlock_car(sio, data):
    try:
        data["access_token"] = GlobalConf.access_token
        uri = "unlock_car"
        # uri = "/cars/unlock"
        # url = "http://127.0.0.1:5000/cars/unlock"
        # print ("the data is:",data)
        # data = urllib.parse.urlencode(data)
        # req = urllib.request.Request(url, data)
        res = sio.emit(
            uri, data, callback=op_unlock_car_callback,
        )
    except Exception as err:
        traceback.print_exc()
        jdata = {
            "error": str(err)
        }
        GlobalConf.recv_queue.put(jdata)


def op_unlock_car_callback(number, data):
    print("op_unlock_car_callback output:", data)
    res = data["unlock_permission"]
    if res is True:
        print("this car has been unlock")
    else:
        print("this car cannot be unlock.")
    GlobalConf.recv_queue.put(data)


def op_return_car(sio, data):
    try:
        data["access_token"] = GlobalConf.access_token
        data["refrsh_token"] = GlobalConf.refrsh_token
        uri = "return_car"
        res = sio.emit(
            uri, data, callback=op_return_car_callback,
        )
    except Exception as err:
        traceback.print_exc()
        jdata = {
            "error": str(err)
        }
        GlobalConf.recv_queue.put(jdata)


def op_return_car_callback(data):
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
    # cmd,data = "login", {"username": "user", "password": "password"}
    try:
        res = sio.emit(
            "login", data, callback=op_login_callback,
        )
    except Exception as err:
        jdata = {
            "error": str(err)
        }
        GlobalConf.recv_queue.put(jdata)


def op_login_callback(data):
    #{'success': True, 'username': '1', 'access_token': 'access_token', 'refresh_token': 'refresh_token'}
    GlobalConf.access_token = data.get("access_token")
    GlobalConf.refresh_token = data.get("refresh_token")
    GlobalConf.recv_queue.put(data)


def client_start(send_queue, recv_queue):
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
