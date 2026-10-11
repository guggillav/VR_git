from flask_jwt_extended import get_jwt_identity

from app.models.user_model import User
from app.views.user_view import UserView


class UserController:

    @staticmethod
    def me():
        user = User.find_by_id(int(get_jwt_identity()))
        if not user:
            return UserView.failure("User not found", 404)
        return UserView.user_response(user)
