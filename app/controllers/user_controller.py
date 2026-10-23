#from flask_jwt_extended import get_jwt_identity

#from app.models.user_model import User
#from app.views.user_view import UserView


#class UserController:

 #   @staticmethod
  #  def me():
   #     user = User.find_by_id(int(get_jwt_identity()))
    #    if not user:
     #       return UserView.failure("User not found", 404)
      #  return UserView.user_response(user)
#

from flask_jwt_extended import get_jwt_identity
from app.models.user_model import User
from app.views.user_view import UserView
from app import db

class UserController:

    # For Normal User - Get Own Profile (with JWT token)
    @staticmethod
    def me():
        try:
            user_id = int(get_jwt_identity())
            user = User.find_by_id(user_id)
            if not user:
                return UserView.failure("User not found", 404)
            return UserView.user_response(user)
        except Exception as e:
            return UserView.failure(f"Invalid token: {str(e)}", 401)

    # For Admin Panel - Get All Users from VR Database
    @staticmethod
    def get_all_users():
        users = User.query.all()
        # Convert to list with all 9 fields from your paper
        data = []
        for u in users:
            data.append({
                "id": u.id,
                "name": u.name,
                "email": u.email,
                "mobile": u.mobile,
                "contact": u.email or u.mobile,
                "total_coins": u.total_coins or 0,
                "total_amount": u.total_amount or 0,
                "bonus_coins": u.bonus_coins or 0,
                "is_otp_verified": u.is_otp_verified,
                "face_verified": u.face_verified,
                "created_date": str(u.created_date),
                "created_time": str(u.created_time),
            })
        return UserView.success_data(data)

    # Get Single User by ID / Email / Mobile
    @staticmethod
    def get_user_by_contact(contact):
        user = User.find_by_email(contact) or User.find_by_mobile(contact) or User.find_by_id(contact)
        if not user:
            return UserView.failure("User not found", 404)
        return UserView.user_response(user)

    # Block / Unblock User - For Admin
    @staticmethod
    def block_user(contact):
        user = User.find_by_email(contact) or User.find_by_mobile(contact) or User.query.get(contact)
        if not user:
            return UserView.failure("User not found", 404)
        
        # Toggle block
        user.is_blocked = not getattr(user, 'is_blocked', False)
        db.session.commit()
        
        status = "Blocked" if user.is_blocked else "Unblocked"
        return UserView.success(f"User {status} successfully")

    # Update Coins - Field 5,6,7 from your paper
    @staticmethod
    def update_coins(contact, coins=10, is_bonus=False):
        user = User.find_by_email(contact) or User.find_by_mobile(contact)
        if not user:
            return UserView.failure("User not found", 404)

        if is_bonus:
            # Field 7: Bonus Coins -> whenever user Referred, bonus will be add
            user.bonus_coins = (user.bonus_coins or 0) + coins
            user.total_coins = (user.total_coins or 0) + coins
        else:
            # Field 5: Total Coins -> Need to update every claim
            user.total_coins = (user.total_coins or 0) + coins
        
        # Field 6: Total Amount
        user.total_amount = user.total_coins * 1
        db.session.commit()
        
        return UserView.success(f"Updated - Coins: {user.total_coins}, Amount: {user.total_amount}, Bonus: {user.bonus_coins}")

# For backward compatibility - if your routes call direct functions (not class)
def get_all_users():
    return User.query.all()

def get_user_by_phone(phone):
    return User.find_by_email(phone) or User.find_by_mobile(phone)

def block_user(phone):
    user = User.find_by_email(phone) or User.find_by_mobile(phone)
    if not user:
        return None
    user.is_blocked = not getattr(user, 'is_blocked', False)
    db.session.commit()
    return user