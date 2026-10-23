from flask import Blueprint, jsonify
admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

@admin_bp.route('/', methods=['GET'])
def admin_home():
    return jsonify({"message": "Admin working"}), 200