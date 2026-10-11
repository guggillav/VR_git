from flask import Blueprint
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)

auth_bp.add_url_rule("/register", view_func=AuthController.register, methods=["POST"])
auth_bp.add_url_rule("/login", view_func=AuthController.login, methods=["POST"])
