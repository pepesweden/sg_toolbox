from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username, email=None, created_at=None, is_active=None, is_admin=False):
        self.id = username
        self.username = username
        self.email = email
        self.created_at = created_at
        #self.is_active = is_active
        self.is_admin = is_admin