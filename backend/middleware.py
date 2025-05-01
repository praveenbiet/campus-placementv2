from functools import wraps
from flask import request, jsonify
import jwt
from routes.auth import SECRET_KEY

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        # Handle OPTIONS request
        if request.method == 'OPTIONS':
            return jsonify({}), 200

        token = None
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({'message': 'Invalid token format'}), 401

        if not token:
            return jsonify({'message': 'Token is missing'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
            current_user = {
                'user_id': data['user_id'],
                'user_type': data['user_type']
            }
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401

        return f(current_user, *args, **kwargs)
    return decorated 