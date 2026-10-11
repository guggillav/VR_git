from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.controllers.user_controller import UserController

user_bp = Blueprint("users", __name__)

user_bp.add_url_rule("/me", view_func=jwt_required()(UserController.me), methods=["GET"])
