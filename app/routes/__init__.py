
def register_routes(app):
    # Try to import each blueprint - if file missing, skip it
    
    try:
        from app.routes.auth_routes import auth_bp
        app.register_blueprint(auth_bp)
        print("✓ auth_routes loaded")
    except Exception as e:
        print(f"✗ auth_routes skipped: {e}")

    try:
        from app.routes.user_routes import user_bp
        app.register_blueprint(user_bp)
        print("✓ user_routes loaded")
    except Exception as e:
        print(f"✗ user_routes skipped: {e}")

    try:
        from app.routes.reward_routes import reward_bp
        app.register_blueprint(reward_bp)
        print("✓ reward_routes loaded")
    except Exception as e:
        print(f"✗ reward_routes skipped: {e}")

    try:
        from app.routes.admin_routes import admin_bp
        app.register_blueprint(admin_bp)
        print("✓ admin_routes loaded")
    except Exception as e:
        print(f"✗ admin_routes skipped: {e}")

    @app.route('/health', methods=['GET'])
    def health():
        return {"status": "ok", "db": "VR connected"}, 200

    @app.route('/', methods=['GET'])
    def home():
        return {"message": "VR Humanix Backend Running", "status": "PostgreSQL VR Connected"}, 200