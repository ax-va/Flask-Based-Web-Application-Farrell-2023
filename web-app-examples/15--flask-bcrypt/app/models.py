from flask_bcrypt import check_password_hash
from flask_login import UserMixin
from . import users_db


class User(UserMixin):

    def __init__(self, user_id):
        self.id = user_id
        # Load the hashed password from the mocked database
        self.hashed_password = users_db[self.id]['hashed_password']

    @property
    def user_info(self):
        return f"user_id: {self.id}"

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return self.user_info


