from flask_login import UserMixin
from . import users_db


class User(UserMixin):

    def __init__(self, user_id):
        self.id = user_id

    def verify_password(self, password):
        return users_db[self.id]['password'] == password
