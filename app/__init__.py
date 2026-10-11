import os
from flask import Flask
from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors


def create_app(env=None):
    env = env or os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name[env])
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/*": {"origins": "*"}})

    # import models so migrations can see them
    from app import models  # noqa: F401

    from app.routes import register_routes
    register_routes(app)

    from app.errors import register_error_handlers
    register_error_handlers(app)

    @app.route("/health")
    def health():
        return {"status": "ok"}

    return app
