""" Authentication """
from logging import getLogger
from urllib.parse import urlparse

from flask import redirect, url_for, render_template, flash, request, current_app
from flask_login import login_user, login_required, logout_user, current_user

from . import auth_bp
from .forms import LoginForm, RegisterNewUserForm, RequestResetPasswordForm, ResetPasswordForm, ResendConfirmationForm
from ..emailer import send_mail
from ..models import db_session_manager, User
from .. import login_manager

logger = getLogger(__name__)


@login_manager.user_loader
def load_user(user_id):
    """ Called every time the login_manager needs to determine if the user exists """
    with db_session_manager() as db_session:
        return db_session.query(User).get(user_id)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    The login handler function:
    - Called by an HTTP GET request -> Return the rendered "login.html" template.
    - Called by an HTTP POST request -> Process the contents of the form parameters in the "login.html" template.
    """
    logger.debug("Logging in...")

    form = LoginForm()
    if form.cancel.data:
        return redirect(url_for("intro_bp.home"))

    if form.validate_on_submit():
        # HTTP POST
        with db_session_manager() as db_session:
            # Get user from the database based on the form email value
            user = db_session.query(User).filter(User.email == form.email.data).one_or_none()
            # Verify user and password
            if user is None or not user.verify_password(form.password.data):
                logger.debug("Invalid email or password.")
                # Append the message to the list of messages available in the context
                # of the next request and only the next request using the Flask flash
                flash("Invalid email or password", "warning")
                # Rerender the login page
                return redirect(url_for("auth_bp.login"))
            # Update the login manager system about the user and creates a session cookie to remember them
            login_user(user, remember=form.remember_me.data)  # Remember the logged-in user between the browser sessions
            logger.debug("Logged in successfully.")
            # Get the page to which the user was trying to navigate
            next_ = request.args.get("next")
            # Validate the request for that page if the "netloc" attribute is valid
            if not next_ or urlparse(next_).netloc != "":
                next_ = url_for("intro_bp.home")
            return redirect(next_)
    # HTTP GET
    return render_template("login.html", form=form)


@auth_bp.get("/register_new_user")
@auth_bp.post("/register_new_user")
def register_new_user():
    """ Handles HTTP GET and HTTP POST requests to register a new user """
    # If the user is already authenticated, redirect them to the homepage
    if current_user.is_authenticated:
        return redirect(url_for("intro_bp.home"))

    form = RegisterNewUserForm()
    if form.cancel.data:
        return redirect(url_for("auth_bp.login"))

    if form.validate_on_submit():
        # HTTP POST
        with db_session_manager() as db_session:
            # Create a new user initializing the attributes with form data
            user = User(
                first_name=form.first_name.data,
                last_name=form.last_name.data,
                email=form.email.data,
                password=form.password.data,
            )
            # Add the newly created user to the database
            db_session.add(user)
            # Commit adding user
            db_session.commit()
            _send_confirmation_email(user)
            timeout = current_app.config.get("CONFIRMATION_LINK_TIMEOUT")
            flash((
                "Please click on the confirmation link just sent "
                f"to your email address within {timeout} hours "
                "to complete your registration"
            ))
            # Log debug message
            logger.debug(f"New user '{form.email.data}' added.")
            # Redirect to the login page
            return redirect(url_for("auth_bp.login"))
    # HTTP GET request to render the page
    return render_template("register_new_user.html", form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    logger.debug("Logged out")
    flash("You've been logged out", "light")
    return redirect(url_for('auth_bp.login'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('auth_bp.login'))


@auth_bp.get("/confirm/<confirmation_token>")
@login_required  # To confirm a token, the user should log in
def confirm(confirmation_token):
    if current_user.confirmed:
        return redirect(url_for("intro_bp.home"))

    try:
        # Can the token be confirmed?
        if current_user.confirm_token(confirmation_token):
            # The user's "confirmed" attribute changed to True
            with db_session_manager() as db_session:
                # Update the user in the database
                db_session.add(current_user)
                db_session.commit()
                flash("Thank you for confirming your account.")
    # The confirmation token is bad or expired
    except Exception as e:
        logger.exception(e)
        flash(str(e))
        # Redirect the user to the resend confirmation page
        return redirect(url_for("auth_bp.resend_confirmation"))
    # Redirect to the home page
    return redirect(url_for("intro_bp.home"))


@auth_bp.get("/resend_confirmation")
@auth_bp.post("/resend_confirmation")
def resend_confirmation():
    form = ResendConfirmationForm()
    if form.cancel.data:
        return redirect(url_for("auth_bp.login"))

    if form.validate_on_submit():
        with db_session_manager() as db_session:
            user = (
                db_session
                .query(User)
                .filter(User.email == form.email.data)
                .one_or_none()
            )
            if user is not None:
                _send_confirmation_email(user)
                timeout = current_app.config.get("CONFIRMATION_LINK_TIMEOUT")
                flash((
                    "Please click on the confirmation link just sent "
                    f"to your email address within {timeout} hours "
                    "to complete your registration"
                ))
                return redirect(url_for("intro_bp.home"))
    return render_template("resend_confirmation.html", form=form)


@auth_bp.get("/request_reset_password")
@auth_bp.post("/request_reset_password")
def request_reset_password():
    if current_user.is_authenticated:
        return redirect("intro_bp.home")

    form = RequestResetPasswordForm()
    if form.cancel.data:
        return redirect(url_for("intro_bp.home"))

    if form.validate_on_submit():
        with db_session_manager() as db_session:
            user = (
                db_session.query(User)
                .filter(User.email == form.email.data)
                .one_or_none()
            )
            if user is not None:
                _send_password_reset(user)
                timeout = current_app.config.get("PASSWORD_RESET_TIMEOUT")
                flash(f"Check your email to reset your password within {timeout} minutes.")
                return redirect(url_for("intro_bp.home"))
    # HTTP GET request to render the page
    return render_template("request_reset_password.html", form=form)


@auth_bp.get("/reset_password/<token>")
@auth_bp.post("/reset_password/<token>")
def reset_password(token):
    if current_user.is_authenticated:
        return redirect("intro_bp.home")

    try:
        user_uid = User.get_user_uid_from_reset_token(token)
        with db_session_manager() as db_session:
            user = (
                db_session
                .query(User)
                .filter(User.user_uid == user_uid)
                .one_or_none()
            )

            if user is None:
                flash("Reset token invalid")
                return redirect("intro_bp.home")

            form = ResetPasswordForm()
            if form.cancel.data:
                return redirect(url_for("intro_bp.home"))

            if form.validate_on_submit():
                # Updates and saves the user's new password
                user.password = form.password.data
                db_session.commit()
                flash("Your password has been reset")
                return redirect(url_for("intro_bp.home"))
    except Exception as e:
        flash(str(e))
        logger.exception(e)
        return redirect("intro_bp.home")
    # HTTP GET request to render the page
    return render_template("reset_password.html", form=form)


def _send_confirmation_email(user: User) -> None:
    """
    Sends a confirmation email to the user to confirm and
    activate their account after registering as a new user.

    Args:
        user: The user to send the email to
    """
    # The confirmation token is unique for each user
    confirmation_token = user.generate_confirmation_token()
    confirmation_url = url_for(
        "auth_bp.confirm",  # to build a URL to a URL handler
        confirmation_token=confirmation_token,  # to build a unique token with an expiration timeout
        _external=True,  # to create a full URL when a user clicks the link from their email client context
    )
    timeout: int = current_app.config.get("CONFIRMATION_LINK_TIMEOUT")
    to = user.email
    subject = "Confirm Your Email"
    contents = (
        f"""Hi {user.first_name}, welcome to AlexBlog,<br/><br/>
        please click the link to confirm your email within {timeout} hours.<br/><br/>
        <a href="{confirmation_url}">Click here to complete registration.</a><br/><br/>
        Thank you!
        """
    )
    send_mail(to=to, subject=subject, contents=contents)


def _send_password_reset(user: User) -> None:
    """
    Sends a password reset email to the user.

    Args:
        user: The database user object
    """
    # Create the encrypted reset token with the expiration timeout
    token = user.generate_reset_token()
    timeout: int = current_app.config.get("PASSWORD_RESET_TIMEOUT")
    to = user.email
    subject = "Password Reset"
    contents = (
        f"""{user.first_name},<br/><br/>
        click the following link to reset your password within {timeout} minutes.
        <a href="{ url_for('auth_bp.reset_password', token=token, _external=True) }">Reset your password.</a>
        <br/><br/>
        If you haven't requested a password reset ignore this email.<br/><br/>
        Best regards,<br/>,
        AlexBlog
        """
    )
    send_mail(to=to, subject=subject, contents=contents)
