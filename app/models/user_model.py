from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---- data access methods (no request / response code here) ----
    @staticmethod
    def find_by_email(email):
        return User.query.filter_by(email=email).first()

    @staticmethod
    def find_by_id(user_id):
        return db.session.get(User, user_id)

    @staticmethod
    def create(name, email, password, role="user"):
        user = User(name=name, email=email, role=role)
        user.password_hash = generate_password_hash(password)
        db.session.add(user)
        db.session.commit()
        return user

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
