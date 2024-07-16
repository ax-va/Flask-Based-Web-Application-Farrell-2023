""" Authentication """
from logging import getLogger
from urllib.parse import urlparse

from flask import redirect, url_for, render_template, flash, request
from flask_login import login_user, login_required, logout_user, current_user

from . import auth_bp
from .forms import LoginForm, RegisterNewUserForm
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
        return redirect(url_for("auth_bp.login"))

    if form.register.data:
        return redirect(url_for("auth_bp.register_new_user"))

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
                next_ = url_for("auth_bp.protected")
            return redirect(next_)

    # HTTP GET
    return render_template("login.html", form=form)


@auth_bp.get("/register_new_user")
@auth_bp.post("/register_new_user")
def register_new_user():
    """ Handles HTTP GET and HTTP POST requests to register a new user """
    # If the user is already authenticated, redirect them to the homepage
    if current_user.is_authenticated:
        return redirect(url_for("auth_bp.protected"))

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
            # Log debug message
            logger.debug(f"New user '{form.email.data}' added.")
            # Redirect to the login page
            return redirect(url_for("auth_bp.login"))
    # HTTP GET
    return render_template("register_new_user.html", form=form)


@auth_bp.route('/protected')
@login_required
def protected():
    logger.debug(f"Logged in as '{current_user.email}'")
    return redirect(url_for("intro_bp.home"))


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
