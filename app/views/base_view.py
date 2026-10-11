from flask import jsonify


class BaseView:

    @staticmethod
    def success(data=None, message="OK", status=200):
        return jsonify({"success": True, "message": message, "data": data}), status

    @staticmethod
    def failure(message="Error", status=400):
        return jsonify({"success": False, "message": message}), status
