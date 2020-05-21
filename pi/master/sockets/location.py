from master import socketio


@socketio.on("location_update")
def location_update(data):
    pass
