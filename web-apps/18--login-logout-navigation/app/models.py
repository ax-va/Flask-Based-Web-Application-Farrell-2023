from contextlib import contextmanager
from datetime import datetime, timezone
from uuid import uuid4
from flask_bcrypt import (
    generate_password_hash,
    check_password_hash,
)
from flask_login import UserMixin
from . import db


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
    created = db.Column(db.DateTime, nullable=False, default=datetime.now(tz=timezone.utc))
    updated = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now(tz=timezone.utc),
        onupdate=datetime.now(tz=timezone.utc),
    )

    def get_id(self):
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
            f"active: {self.active}"
        )

    def verify_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return self.user_info
