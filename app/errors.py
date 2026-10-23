# app/errors.py

from flask import jsonify

def register_error_handlers(app):

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "message": "Bad Request - Check your data"}), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({"success": False, "message": "Unauthorized - Please login again"}), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"success": False, "message": "API not found - Check URL"}), 404

    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"success": False, "message": "Server Error in VR Backend"}), 500

    # For JWT errors
    @app.errorhandler(422)
    def jwt_error(error):
        return jsonify({"success": False, "message": "Invalid Token"}), 422