from flask_login import UserMixin
from . import users_db


class User(UserMixin):

    def __init__(self, user_id):
        self.id = user_id

    @property
    def user_info(self):
        return f"user_id: {self.id}\n"

    def verify_password(self, password):
        return users_db[self.id]['password'] == password

    def __repr__(self):
        return self.user_info


