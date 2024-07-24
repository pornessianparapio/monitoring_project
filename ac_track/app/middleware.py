from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps

def jwt_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            # Verifies the JWT in the request cookies
            verify_jwt_in_request()
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify(message=str(e)), 401
    return wrapper

def get_current_user():
    try:
        # Extracts the current user's identity from the JWT
        user_identity = get_jwt_identity()
        return user_identity
    except Exception as e:
        return None
