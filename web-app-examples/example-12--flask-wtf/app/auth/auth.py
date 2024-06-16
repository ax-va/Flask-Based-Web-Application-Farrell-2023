from logging import getLogger

from flask import redirect, url_for, request, render_template
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
        user = User(request.form['email'])
        # Verify user ID and password
        if user.id not in users_db or not user.verify_password(request.form['password']):
            logger.debug("Invalid email or password.")
            return redirect(url_for("auth_bp.login"))

        login_user(user)
        logger.debug("Logged in successfully.")
        return redirect(url_for("auth_bp.protected"))

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
    return redirect(url_for('auth_bp.login'))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('auth_bp.login'))
