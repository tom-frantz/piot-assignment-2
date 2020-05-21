def success_response(**params):
    return {"success": True, **params}


def error_response(msg):
    return {"success": False, "message": msg}
