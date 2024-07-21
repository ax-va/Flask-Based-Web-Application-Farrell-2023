from contextlib import contextmanager
from datetime import datetime, timezone, timedelta
from time import time
from uuid import uuid4

import jwt
from flask import current_app
from flask_bcrypt import (
    generate_password_hash,
    check_password_hash,
)
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

from . import db

CONFIRMATION_LINK_TIMEOUT: int = current_app.config.get("CONFIRMATION_LINK_TIMEOUT") * 60 * 1000  # milliseconds
PASSWORD_RESET_TIMEOUT: int = current_app.config.get("PASSWORD_RESET_TIMEOUT") * 60  # seconds


@contextmanager
def db_session_manager(session_close=True):
    """
    Creates a database session with a context manager
    and assure closing the session at the end of the scope.

    Yields:
        Session: The database session object to use
    """
    try:
        yield db.session
    except Exception as e:
        db.session.rollback()
        raise e
    finally:
        if session_close:
            db.session.close()


def get_uuid():
    """
    Create a UUID value and then return the hex string
    version of that value that is unique worldwide.
    """
    return uuid4().hex


class User(UserMixin, db.Model):
    """
    The User class multiply inherits from the UserMixin and db.Model classes.

    ORM = Object-Relational Mapping

    This class will correspond to the table,
    the instances of this class will correspond to the rows of the table,
    and the class attributes correspond to the columns of the table.
    """
    # Define the table name in the database
    __tablename__ = "users"
    # Define the unique ID value for User records using the get_uuid function
    user_uid = db.Column(db.String, primary_key=True, default=get_uuid)
    # Define other User attributes
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True, index=True)
    hashed_password = db.Column("password", db.String, nullable=False)
    active = db.Column(db.Boolean, nullable=False, default=True)
    confirmed = db.Column(db.Boolean, default=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=timezone.utc))
    updated = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc),
    )

    def get_id(self) -> str:
        """
        Overrides the default behavior of the method in the UserMixin class that returns "self.id"
        """
        return self.user_uid

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
            f"user_uid: {self.user_uid}\n"
            f"name: {self.first_name} {self.last_name}\n"
            f"email: {self.email}\n"
            f"confirmed: {self.confirmed}\n"
            f"active: {self.active}"
        )

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def generate_confirmation_token(self) -> str:
        """
        Generates a confirmation token using Flask SECRET_KEY,
        the current timestamp for timeout, and the user's UID.

        Returns:
            string token
        """
        # Create a serializing instance based on the Flask SECRET_KEY
        # including the *current timestamp*
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        # <itsdangerous.url_safe.URLSafeTimedSerializer at ...>
        # Create the unique token based on the new user's user_uid value
        # like 'eyJjb25maXJtIjoiZmdta2xtYmRndHdrazEyMzN2bmZoZmoyMzRr...'
        return serializer.dumps({"confirm": self.user_uid})

    def confirm_token(self, token: str) -> bool:
        """
        Confirms that a token received in response to clicking the link in the email
        is valid to verify that the user completed the registration process.
        Changes the confirmed attribute to True.
        """
        serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
        try:
            data = serializer.loads(token, max_age=CONFIRMATION_LINK_TIMEOUT)
            if data.get("confirm") != self.user_uid:
                return False
            self.confirmed = True
            return True
        except (SignatureExpired, BadSignature) as e:
            raise e

    def generate_reset_token(self) -> str:
        """
        Generates a reset token using Flask SECRET_KEY, the user's UID, and timeout.

        Returns:
            string token
        """
        return jwt.encode(
            {
                "reset_password": self.user_uid,
                "exp": time() + PASSWORD_RESET_TIMEOUT,
            },
            current_app.config["SECRET_KEY"],
            algorithm="HS256"
        )

    @staticmethod
    def get_user_uid_from_reset_token(token: str) -> str:
        """
        Gets the user' UID from the reset token.

        Args:
            token: reset token

        Returns:
            the user's UID
        """

        user_uid = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )["reset_password"]
        return user_uid

    def __repr__(self):
        return self.user_info
