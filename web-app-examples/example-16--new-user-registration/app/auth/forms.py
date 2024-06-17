from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SubmitField
from wtforms.fields.simple import EmailField, StringField
# field validation classes used to validate the form elements
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from .. import users_db


class LoginForm(FlaskForm):
    """
    Defines the WTForm class inheriting from the base FlaskForm class,
    an instance of which is passed to the login template.
    """
    # Create the email form element and validators
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Length(
                min=4,
                max=128,
                message="Email must be between 4 and 128 characters long",
            ),
            Email()
        ],
        render_kw={
            "placeholder": " ",  # Make the Bootstrap styling input element's visual functionality work as intended
            "tabindex": 1,
            "autofocus": True,
        },
    )
    # Create the password form element and validators
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(
                min=6,
                max=64,
                message="Password must be between 6 and 64 characters long",
            ),
        ],
        render_kw={
            "placeholder": " ",  # Make the Bootstrap styling input element's visual functionality work as intended
            "tabindex": 2,
        },
    )
    # Create the "remember_me" form element
    remember_me = BooleanField(
        " Keep me logged in",
        render_kw={"tabindex": 3},
    )
    # Creates the form Log In button
    login = SubmitField(
        "Log In",
        render_kw={"tabindex": 4},
    )
    register = SubmitField(
        "Register",
        render_kw={"tabindex": 5},
    )
    # Create the form Cancel button
    cancel = SubmitField(
        "Cancel",
        render_kw={"tabindex": 6},
    )


class RegisterNewUserForm(FlaskForm):
    """
    Defines a WTForm class inheriting from the base FlaskForm class,
    an instance of which is passed to the register-new-user template.
    """
    # Create form elements
    first_name = StringField(
        "First Name",
        validators=[DataRequired()],
        render_kw={
            "placeholder": " ",
            "tabindex": 1,
            "autofocus": True,
        }
    )
    last_name = StringField(
        "Last Name",
        validators=[DataRequired()],
        render_kw={
            "placeholder": " ",
            "tabindex": 2,
        }
    )
    email = EmailField(
        "Email",
        validators=[
            DataRequired(),
            Length(
                min=4,
                max=128,
                message="Email must be between 4 and 128 characters long"
            ),
            Email()
        ],
        render_kw={
            "placeholder": " ",
            "tabindex": 3,
        }
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(
                min=6,
                max=64,
                message="Password must be between 6 and 64 characters long"
            ),
        ],
        render_kw={
            "placeholder": " ",
            "tabindex": 4,
        }
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            Length(
                min=6,
                max=64,
                message="Password must be between 6 and 64 characters long"
            ),
            EqualTo("password", message="Passwords must match")
        ],
        render_kw={
            "placeholder": " ",
            "tabindex": 5,
        }
    )
    # Create submit buttons
    create_new_user = SubmitField(
        "Create New User",
        render_kw={"tabindex": 6},
    )
    cancel = SubmitField(
        "Cancel",
        render_kw={"tabindex": 7},
    )

    def validate_email(self, email_field):
        """
        Ensures a new user isn't using an email address that already exists in the database.
        This method is introspected by the functionality of the FlaskForm class inherited
        and added to the validation for the email form field.
        """
        if email_field.data in users_db:
            raise ValidationError("Email already registered.")
