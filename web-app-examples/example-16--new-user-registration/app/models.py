from flask_bcrypt import check_password_hash, generate_password_hash
from flask_login import UserMixin
from . import users_db


class User(UserMixin):
    def __init__(self, **kwargs):
        if 'user_id' in kwargs and kwargs['user_id'] in users_db:
            # Load user data from the mocked database
            self.id = kwargs['user_id']
            self.first_name = users_db[self.id]['first_name']
            self.last_name = users_db[self.id]['last_name']
            self.email = users_db[self.id]['email']
            # Load the hashed password from the mocked database
            self.hashed_password = users_db[self.id]['hashed_password']
        else:
            # Create user
            if (
                    kwargs is None
                    or ('first_name' not in kwargs)
                    or ('last_name' not in kwargs)
                    or ('email' not in kwargs)
                    or ('password' not in kwargs)
            ):
                raise AttributeError("Cannot create a user.")
            self.id = kwargs['email']
            self.first_name = kwargs['first_name']
            self.last_name = kwargs['last_name']
            self.email = kwargs['email']
            self.password = kwargs['password']  # Password is hashed and stored in self.hashed_password

    @property
    def password(self):
        """ Write-only attribute """
        raise AttributeError("The user password is a write-only attribute.")

    @password.setter
    def password(self, new_password):
        """ Write-only attribute """
        # Generates a cryptographically strong hash of the password
        self.hashed_password = generate_password_hash(new_password)

    @property
    def user_info(self):
        return (
            f"user_id: {self.id}\n"
            f"first_name: {self.first_name}\n"
            f"last_name: {self.last_name}\n"
            f"email: {self.email }"
        )

    def add_to_db(self):
        """ Add user to the mocked database """
        users_db[self.id] = {
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'hashed_password': self.hashed_password,
        }

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return self.user_info


