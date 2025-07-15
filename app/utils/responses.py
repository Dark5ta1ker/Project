from flask import jsonify

def json_response(data=None, message='', status=200, error=None):
    response = {
        'status': 'success' if 200 <= status < 300 else 'error',
        'data': data,
        'message': message
    }
    if error:
        response['error'] = error
    return jsonify(response), status