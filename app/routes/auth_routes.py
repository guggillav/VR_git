from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, date
import random
from app.extensions import db
from app.models.user_model import User
from flask_mail import Message

auth_bp = Blueprint('auth', __name__)

def parse_contact(contact):
    if '@' in contact:
        return {'email': contact, 'mobile': None}
    else:
        return {'email': None, 'mobile': contact}
    
def send_otp_email(to_email, otp):
    try:
        if '@' not in to_email or 'humanix.local' in to_email:
            print(f"Skipping email for mobile/local: {to_email}, OTP: {otp}")
            return False
        from app import mail
        msg = Message(
            subject="VR Humanix - Your OTP Code",
            recipients=[to_email],
            body=f"Hello!\n\nYour OTP for VR Humanix is: {otp}\nValid for 5 minutes.\n\nThank you!"
        )
        mail.send(msg)
        print(f"✓ OTP Email sent to {to_email}: {otp}")
        return True
    except Exception as e:
        print(f"✗ Email failed: {e}, but OTP is {otp} for {to_email}")
        return False
    
@auth_bp.route('/api/auth/create-account', methods=['POST'])
def create_account():
    data = request.get_json()
    if not data:
        return jsonify({"success": False, "message": "No data"}), 400
    
    contact = data.get('email') or data.get('contact') or ""
    password = data.get('password') or ""
    name = data.get('name') or contact  # No first/last name needed here now!
    
    if not contact or not password:
        return jsonify({"success": False, "message": "Email/Mobile and password required"}), 400
    
    parsed = parse_contact(contact)
    email = parsed['email'] or (contact if '@' in contact else f"{contact}@humanix.local")
    mobile = parsed['mobile']
    otp = str(random.randint(100000, 999999))
    
    existing = User.query.filter_by(email=email).first()
    if existing:
        # FIX 1: If already fully verified, block re-creation
        if existing.is_otp_verified and existing.face_verified:
            return jsonify({
                "success": False,
                "already_exists": True,
                "message": "Account already exists, please login"
            }), 400
        
        # If not verified yet, allow resend OTP
        existing.password_hash = generate_password_hash(password)
        if data.get('name') and data.get('name') != contact:
            existing.name = name
        existing.otp_code = otp
        existing.is_otp_verified = False
        db.session.commit()
        send_otp_email(email, otp)
        return jsonify({"success": True, "message": f"OTP resent to {email}", "otp": otp, "name": existing.name})
    
    new_user = User(
        email=email,
        mobile=mobile,
        password_hash=generate_password_hash(password),
        name=name, # Temporary name = email, will be updated from Create Profile page
        otp_code=otp,
        is_otp_verified=False,
        face_verified=False,
        total_coins=0,
        total_amount=0,
        bonus_coins=0,
        created_date=date.today(),
        created_time=datetime.now().time(),
        created_at=datetime.utcnow()
    )
    
    db.session.add(new_user)
    db.session.commit()
    send_otp_email(email, otp)
    
    return jsonify({
        "success": True, 
        "message": f"Account created, OTP sent to {email}",
        "otp": otp,
        "user_id": new_user.id,
        "name": name
    }), 200

# FIX 2: NEW ROUTE - For Create Profile page (Full Name + Username)
@auth_bp.route('/api/auth/update-profile', methods=['POST'])
def update_profile():
    data = request.get_json()
    contact = data.get('email') or data.get('contact') or ""
    name = data.get('name') or ""
    username = data.get('username') or ""

    if not contact or not name:
        return jsonify({"success": False, "message": "Email and name required"}), 400

    parsed = parse_contact(contact)
    email = parsed['email'] or (contact if '@' in contact else f"{contact}@humanix.local")

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    user.name = name
    # If you have username field in model, uncomment:
    # if hasattr(user, 'username'):
    #     user.username = username
    db.session.commit()

    print(f"✅ Profile updated: {email} -> Name: {name}, Username: {username}")
    return jsonify({"success": True, "message": "Profile updated", "name": name, "username": username})

# --- REST SAME ---
@auth_bp.route('/api/auth/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    contact = data.get('email') or data.get('contact') or ""
    otp_code = data.get('otp_code') or data.get('otp') or ""
    if not contact or not otp_code:
        return jsonify({"success": False, "message": "Contact and OTP required"}), 400
    parsed = parse_contact(contact)
    email = parsed['email'] or (contact if '@' in contact else f"{contact}@humanix.local")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    if str(user.otp_code) == str(otp_code):
        user.is_otp_verified = True
        db.session.commit()
        return jsonify({"success": True, "message": "OTP Verified"})
    else:
        return jsonify({"success": False, "message": "Invalid OTP"}), 400

@auth_bp.route('/api/auth/face-verification', methods=['POST'])
def face_verification():
    data = request.get_json()
    contact = data.get('email') or data.get('contact') or ""
    parsed = parse_contact(contact)
    email = parsed['email'] or (contact if '@' in contact else f"{contact}@humanix.local")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404
    user.face_verified = True
    db.session.commit()
    return jsonify({"success": True, "message": "Face Verified"})

@auth_bp.route('/api/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    contact = data.get('email') or data.get('contact') or ""
    password = data.get('password') or ""
    if not contact or not password:
        return jsonify({"status": "Invalid", "message": "Contact and password required"}), 400
    parsed = parse_contact(contact)
    email = parsed['email'] or (contact if '@' in contact else f"{contact}@humanix.local")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"status": "Invalid", "message": "No account found"}), 401
    if not check_password_hash(user.password_hash, password):
        return jsonify({"status": "Invalid", "message": "Wrong password"}), 401
    return jsonify({"status": "valid","message": "Open APP","user": {"id": user.id,"email": user.email,"name": user.name,"mobile": user.mobile,"total_coins": user.total_coins}}), 200

@auth_bp.route('/api/auth/claim-coins', methods=['POST'])
def claim_coins():
    data = request.get_json()
    contact = data.get('email') or ""
    coins = data.get('coins', 10)
    parsed = parse_contact(contact)
    email = parsed['email'] or (contact if '@' in contact else f"{contact}@humanix.local")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False}), 404
    user.total_coins = (user.total_coins or 0) + coins
    user.total_amount = user.total_coins
    db.session.commit()
    return jsonify({"success": True, "total_coins": user.total_coins, "total_amount": user.total_amount})

@auth_bp.route('/api/auth/refer-bonus', methods=['POST'])
def refer_bonus():
    data = request.get_json()
    contact = data.get('email') or ""
    parsed = parse_contact(contact)
    email = parsed['email'] or (contact if '@' in contact else f"{contact}@humanix.local")
    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False}), 404
    user.bonus_coins = (user.bonus_coins or 0) + 50
    user.total_coins = (user.total_coins or 0) + 50
    user.total_amount = user.total_coins
    db.session.commit()
    return jsonify({"success": True, "total_coins": user.total_coins, "bonus_coins": user.bonus_coins})

@auth_bp.route('/api/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    result = []
    for u in users:
        result.append({
            "id": u.id,
            "email": u.email,
            "mobile": u.mobile,
            "name": u.name,
            "contact": u.email or u.mobile,
            "total_coins": u.total_coins or 0,
            "total_amount": u.total_amount or 0,
            "bonus_coins": u.bonus_coins or 0,
            "is_otp_verified": u.is_otp_verified,
            "face_verified": u.face_verified,
            "created_date": str(u.created_date) if u.created_date else "",
            "created_time": str(u.created_time) if u.created_time else "",
            "created_at": str(u.created_at) if u.created_at else ""
        })
    return jsonify(result)

@auth_bp.route('/api/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    u = User.query.get(id)
    if u:
        db.session.delete(u)
        db.session.commit()
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "User not found"}), 404

@auth_bp.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "vr": "connected"})