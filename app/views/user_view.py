from app.views.base_view import BaseView


class UserView(BaseView):

    @staticmethod
    def render_user(user):
        """Controls exactly which fields leave the server (never the password hash)."""
        return {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.strftime("%d-%m-%Y") if user.created_at else None,
        }

    @classmethod
    def user_response(cls, user, message="OK", status=200):
        return cls.success(cls.render_user(user), message, status)

    @classmethod
    def login_response(cls, user, token):
        return cls.success({"token": token, "user": cls.render_user(user)}, "Login successful")
