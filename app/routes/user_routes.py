#from flask import Blueprint
#from flask_jwt_extended import jwt_required
#from app.controllers.user_controller import UserController

#user_bp = Blueprint("users", __name__)

#user_bp.add_url_rule("/me", view_func=jwt_required()(UserController.me), methods=["GET"])

from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from app.controllers.user_controller import get_all_users, get_user_by_phone

user_bp = Blueprint('user', __name__)

@user_bp.route('/api/users', methods=['GET'])
@jwt_required()
def list_users():
    users = get_all_users()
    return jsonify([{"phone": u.phone, "name": u.name, "points": u.points, "is_blocked": u.is_blocked} for u in users])

@user_bp.route('/api/user/<phone>', methods=['GET'])
@jwt_required()
def get_user(phone):
    user = get_user_by_phone(phone)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"phone": user.phone, "name": user.name, "points": user.points})