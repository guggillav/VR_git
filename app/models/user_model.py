#from datetime import datetime
#from werkzeug.security import generate_password_hash, check_password_hash
#from app.extensions import db


#class User(db.Model):
 #   __tablename__ = "users"

    #id = db.Column(db.Integer, primary_key=True)
    #name = db.Column(db.String(100), nullable=False)
    #email = db.Column(db.String(120), unique=True, nullable=False)
    #password_hash = db.Column(db.String(255), nullable=False)
    #role = db.Column(db.String(30), default="user")
    #created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ---- data access methods (no request / response code here) ----
    #@staticmethod
    #def find_by_email(email):
     #   return User.query.filter_by(email=email).first()

    #@staticmethod
    #def find_by_id(user_id):
     #   return db.session.get(User, user_id)

    #@staticmethod
    #def create(name, email, password, role="user"):
      #  user = User(name=name, email=email, role=role)
        #user.password_hash = generate_password_hash(password)
        #db.session.add(user)
        #db.session.commit()
       # return user

    #def verify_password(self, password):
       # return check_password_hash(self.password_hash, password)

from app.extensions import db
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = 'users'  # FIXED: Your pgAdmin table is "user" not "users"!
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    mobile = db.Column(db.String(20), nullable=True)
    name = db.Column(db.String(100), nullable=True)  # Full Name: First + Last
    username = db.Column(db.String(100), nullable=True)  # FIXED: Added for @venky123
    password_hash = db.Column(db.String(255), nullable=False) # FIXED: Was 30, now 255!
    
    otp_code = db.Column(db.String(10), nullable=True)
    is_otp_verified = db.Column(db.Boolean, default=False)
    face_verified = db.Column(db.Boolean, default=False)
    
    total_coins = db.Column(db.Integer, default=0)
    total_amount = db.Column(db.Integer, default=0)
    bonus_coins = db.Column(db.Integer, default=0)
    
    created_date = db.Column(db.Date, default=date.today)
    created_time = db.Column(db.Time, default=lambda: datetime.now().time())
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @classmethod
    def find_by_email(cls, email):
        if not email:
            return None
        return cls.query.filter_by(email=email.lower().strip()).first()

    @classmethod
    def find_by_mobile(cls, mobile):
        if not mobile:
            return None
        return cls.query.filter_by(mobile=mobile.strip()).first()

    @classmethod
    def find_by_id(cls, user_id):
        try:
            return db.session.get(cls, int(user_id))
        except:
            return None

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "mobile": self.mobile,
            "username": self.username, # Added
            "contact": self.email or self.mobile,
            "total_coins": self.total_coins or 0,
            "total_amount": self.total_amount or 0,
            "bonus_coins": self.bonus_coins or 0,
            "is_otp_verified": self.is_otp_verified,
            "face_verified": self.face_verified,
            "created_date": str(self.created_date) if self.created_date else "",
            "created_time": str(self.created_time) if self.created_time else "",
            "created_at": str(self.created_at) if self.created_at else "",
        }