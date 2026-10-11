def register_routes(app):
    from app.routes.auth_routes import auth_bp
    from app.routes.user_routes import user_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    # add new modules here, e.g.:
    # app.register_blueprint(rfq_bp, url_prefix="/api/rfq")
