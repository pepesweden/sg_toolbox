from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username, email=None, created_at=None, active_user=None, is_admin=False):
        self.id = username
        self.username = username
        self.email = email
        self.created_at = created_at
        self.active_user = active_user
        self.is_admin = is_admin