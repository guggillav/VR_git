#from flask import request
#from flask_jwt_extended import create_access_token

#from app.models.user_model import User
f#rom app.views.user_view import UserView


#class AuthController:

    #@staticmethod
    #def register():
        #data = request.get_json(silent=True) or {}

        #missing = [f for f in ("name", "email", "password") if not data.get(f)]
        #if missing:
         #   return UserView.failure(f"Missing: {', '.join(missing)}", 400)

        #if User.find_by_email(data["email"]):
       #     return UserView.failure("Email already registered", 400)

      #  user = User.create(data["name"], data["email"], data["password"])
     #   return UserView.user_response(user, "Registered successfully", 201)

    #@staticmethod
    #def login():
   #     data = request.get_json(silent=True) or {}

  #      user = User.find_by_email(data.get("email", ""))
 #       if not user or not user.verify_password(data.get("password", "")):
#            return UserView.failure("Invalid email or password", 401)

        #token = create_access_token(identity=str(user.id))
        #return UserView.login_response(user, token)

from flask import request
from flask_jwt_extended import create_access_token
from app.models.user_model import User
from app.views.user_view import UserView
from app import db
import random

class AuthController:

    # POINT 1: New User Create Account - As per your paper
    @staticmethod
    def register():
        data = request.get_json(silent=True) or {}

        # Field 1: email or mobile, Field 2: password, Field 3: name optional
        missing = [f for f in ("email", "password") if not data.get(f)]
        if missing:
            return UserView.failure(f"Missing: {', '.join(missing)}", 400)

        contact = data["email"].strip().lower() # can be email or mobile
        
        # Check if user exists in VR DB
        if User.find_by_email(contact) or User.find_by_mobile(contact):
            return UserView.failure("Email/Mobile already registered", 400)

        # Generate OTP - Field 3 from paper
        otp = str(random.randint(100000, 999999))
        
        # Create user - Flask Backend -> PostgreSQL VR store
        user = User.create(
            name=data.get("name", ""),
            email=contact if "@" in contact else None,
            mobile=contact if contact.isdigit() or "@" not in contact else None,
            password=data["password"],
            otp_code=otp
        )
        
        print(f"OTP for {contact}: {otp}") # You will see in terminal
        return UserView.user_response(user, f"Registered successfully. OTP: {otp}", 201)

    # OTP Verification - Field 3
    @staticmethod
    def verify_otp():
        data = request.get_json(silent=True) or {}
        contact = data.get("email", "").strip().lower()
        otp_input = data.get("otp_code", "")

        user = User.find_by_email(contact) or User.find_by_mobile(contact)
        if not user:
            return UserView.failure("User not found", 404)
        
        if user.otp_code != otp_input:
            return UserView.failure("Invalid OTP code", 400)

        user.is_otp_verified = True
        db.session.commit()
        return UserView.success("OTP verified, now do face verification")

    # Face Verification - Field 4
    @staticmethod
    def face_verification():
        data = request.get_json(silent=True) or {}
        contact = data.get("email", "").strip().lower()

        user = User.find_by_email(contact) or User.find_by_mobile(contact)
        if not user:
            return UserView.failure("User not found", 404)

        user.face_verified = True
        db.session.commit()
        return UserView.success("Face verified successfully - User fully stored in VR")

    # POINT 2: User Login - As per your paper
    @staticmethod
    def login():
        data = request.get_json(silent=True) or {}

        contact = data.get("email", "").strip().lower()
        password = data.get("password", "")

        # Find by email OR mobile
        user = User.find_by_email(contact) or User.find_by_mobile(contact)
        
        # Flask verifies user enter details, validate credentials
        if not user or not user.verify_password(password):
            return UserView.failure("Invalid - Invalid email/mobile or password", 401)

        # Check if user completed OTP + Face as per your flow
        if not user.is_otp_verified:
            return UserView.failure("Please verify OTP first", 401)
        if not user.face_verified:
            return UserView.failure("Please complete face verification", 401)

        # valid -> open APP
        token = create_access_token(identity=str(user.id))
        return UserView.login_response(user, token)

    # POINT 3: Claim Coins - Field 5,6,7
    @staticmethod
    def claim_coins():
        data = request.get_json(silent=True) or {}
        contact = data.get("email", "")
        coins = data.get("coins", 10)

        user = User.find_by_email(contact) or User.find_by_mobile(contact)
        if not user:
            return UserView.failure("User not found", 404)

        user.total_coins = (user.total_coins or 0) + coins
        user.total_amount = user.total_coins * 1  # 1 coin = 1 Rs
        db.session.commit()
        return UserView.success(f"Total Coins: {user.total_coins}, Total Amount: {user.total_amount}")
