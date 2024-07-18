""" Authentication """
from logging import getLogger
from urllib.parse import urlparse

from flask import redirect, url_for, render_template, flash, request
from flask_login import login_user, login_required, logout_user, current_user

from . import auth_bp
from .forms import LoginForm
from ..models import User
from .. import login_manager, users_db

logger = getLogger(__name__)


@login_manager.user_loader
def load_user(user_id):
    """ Called every time the login_manager needs to determine if the user exists """
    if user_id not in users_db:
        return

    user = User(user_id)
    return user


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

    if form.validate_on_submit():
        # HTTP POST
        user = User(form.email.data)
        # Verify user ID and password
        if user.id not in users_db or not user.verify_password(form.password.data):
            logger.debug("Invalid email or password.")
            # Append the message to the list of messages available in the context
            # of the next request and only the next request using the Flask flash
            flash("Invalid email or password", "warning")
            return redirect(url_for("auth_bp.login"))

        login_user(user, remember=form.remember_me.data)  # Remember the logged-in user between the browser sessions
        logger.debug("Logged in successfully.")
        next_ = request.args.get("next")
        if not next_ or urlparse(next_).netloc != "":
            next_ = url_for("auth_bp.protected")
        return redirect(next_)

    # HTTP GET
    return render_template("login.html", form=form)


@auth_bp.route('/protected')
@login_required
def protected():
    logger.debug(f"Logged in as '{current_user.id}'")
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
