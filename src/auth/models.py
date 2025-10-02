from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, username, email=None, created_at=None):
        self.id = username
        self.username = username
        self.email = email
        self.created_at = created_at