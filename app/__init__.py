import os
from flask import Flask, send_from_directory
from app.config import config_by_name
from app.extensions import db, migrate, jwt, cors
from flask_mail import Mail

# Create mail instance - for OTP emails
mail = Mail()

def create_app(env=None):
    env = env or os.getenv("FLASK_ENV", "development")
    app = Flask(__name__)
    app.config.from_object(config_by_name[env])

    # Make sure upload folder exists
    os.makedirs(app.config.get("UPLOAD_FOLDER", "uploads"), exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    #cors.init_app(app, resources={r"/": {"origins": ""}})
    cors.init_app(app, resources={r"/": {"origins": "", "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"], "allow_headers": ["Content-Type", "Authorization"]}}, supports_credentials=True)

    # Init Mail - IMPORTANT FOR OTP
    mail.init_app(app)

    # import models so migrations can see them - VERY IMPORTANT FOR VR
    from app import models # noqa: F401

    from app.routes import register_routes
    register_routes(app)

    from app.errors import register_error_handlers
    register_error_handlers(app)

    @app.route('/app')
    def serve_frontend():
        possible_paths = [
            os.getcwd(),
            os.path.join(os.getcwd(), "VR", "VS Code"),
            os.path.join(os.path.dirname(os.getcwd()), "VR", "VS Code"),
            "C:/Users/Venkatesh/Desktop/VR/VS Code",
            "C:/Users/Venkatesh/Desktop/VR/Py/my_project_backend"
        ]
        for folder in possible_paths:
            file_path = os.path.join(folder, "HVUntitled-2.html")
            if os.path.exists(file_path):
                return send_from_directory(folder, "HVUntitled-2.html")
        
        return f"File HVUntitled-2.html not found! I checked: {possible_paths}. Please copy file to: {os.getcwd()}", 404

    @app.route('/open-app')
    def open_app_link():
        return '<script>window.location.href="/app";</script><p>Opening HV App... <a href="/app">Click if not opening</a></p>'

    return app 
