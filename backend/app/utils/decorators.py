from functools import wraps

from flask import jsonify
from flask_jwt_extended import get_jwt, jwt_required


def admin_required():
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != "admin":
                return jsonify({"error": "Admin access required."}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator


def student_required():
    def decorator(fn):
        @wraps(fn)
        @jwt_required()
        def wrapper(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") not in {"student", "admin"}:
                return jsonify({"error": "Access denied."}), 403
            return fn(*args, **kwargs)

        return wrapper

    return decorator
