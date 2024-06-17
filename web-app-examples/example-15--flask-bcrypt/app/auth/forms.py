from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, SubmitField
from wtforms.fields.simple import EmailField
# field validation classes used to validate the form elements
from wtforms.validators import DataRequired, Email, Length


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
    # Create the form Cancel button
    cancel = SubmitField(
        "Cancel",
        render_kw={"tabindex": 5},
    )
