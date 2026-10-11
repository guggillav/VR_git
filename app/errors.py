import logging
from app.views.base_view import BaseView


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found(e):
        return BaseView.failure("Resource not found", 404)

    @app.errorhandler(405)
    def method_not_allowed(e):
        return BaseView.failure("Method not allowed", 405)

    @app.errorhandler(500)
    def server_error(e):
        logging.exception("Server error")
        return BaseView.failure("Internal server error", 500)
