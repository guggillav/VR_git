from flask import request
from flask_jwt_extended import create_access_token

from app.models.user_model import User
from app.views.user_view import UserView


class AuthController:

    @staticmethod
    def register():
        data = request.get_json(silent=True) or {}

        missing = [f for f in ("name", "email", "password") if not data.get(f)]
        if missing:
            return UserView.failure(f"Missing: {', '.join(missing)}", 400)

        if User.find_by_email(data["email"]):
            return UserView.failure("Email already registered", 400)

        user = User.create(data["name"], data["email"], data["password"])
        return UserView.user_response(user, "Registered successfully", 201)

    @staticmethod
    def login():
        data = request.get_json(silent=True) or {}

        user = User.find_by_email(data.get("email", ""))
        if not user or not user.verify_password(data.get("password", "")):
            return UserView.failure("Invalid email or password", 401)

        token = create_access_token(identity=str(user.id))
        return UserView.login_response(user, token)
