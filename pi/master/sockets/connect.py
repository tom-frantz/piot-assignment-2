from master import socketio


@socketio.on("my event")
def my_event(*args, **kwargs):
    print("We received an event")
    return {"ok": "baby"}
