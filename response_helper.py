from flask import jsonify

def success_response(data=None, message=None, code=200, pagination=None):
    payload = {"status": "success"}
    if message:
        payload["message"] = message
    if data is not None:
        payload["data"] = data
    if pagination is not None:
        payload["pagination"] = pagination
    return jsonify(payload), code

def fail_response(errors, code=400):
    return jsonify({
        "status": "fail",
        "errors": errors
    }), code

def error_response(message="Terjadi kesalahan internal server", code=500):
    return jsonify({
        "status": "error",
        "message": message
    }), code
