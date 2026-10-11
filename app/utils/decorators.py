from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

from app.models.user_model import User
from app.views.base_view import BaseView


def role_required(*roles):
    """Usage: @role_required('admin')"""
    def wrapper(fn):
        @wraps(fn)
        def decorated(*args, **kwargs):
            verify_jwt_in_request()
            user = User.find_by_id(int(get_jwt_identity()))
            if not user or user.role not in roles:
                return BaseView.failure("Forbidden", 403)
            return fn(*args, **kwargs)
        return decorated
    return wrapper
