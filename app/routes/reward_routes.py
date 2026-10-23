from flask import Blueprint, jsonify
reward_bp = Blueprint('reward', __name__, url_prefix='/api/rewards')

@reward_bp.route('/', methods=['GET'])
def get_rewards():
    return jsonify({"message": "Rewards working"}), 200