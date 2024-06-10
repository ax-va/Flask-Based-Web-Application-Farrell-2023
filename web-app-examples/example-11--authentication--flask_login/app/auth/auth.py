from logging import getLogger
from urllib.parse import urlparse

from flask import redirect, url_for, request, render_template
from flask_login import login_user, login_required, logout_user, current_user

from . import auth_bp
from ..models import User
from .. import login_manager

logger = getLogger(__name__)

# Mock database
users = {'ax-va@some-company.com': {'password': 'secret'}}


@login_manager.user_loader
def user_loader(user_id):
    """ Called every time the login_manager needs to determine if the user exists """
    if user_id not in users:
        return

    user = User()
    user.id = user_id
    return user


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """ Handles HTTP GET and HTTP POST requests """
    logger.debug("Logging in...")
    if request.method == 'GET':
        return render_template("login.html")

    user = User()
    user.id = request.form['email']
    # Verify user ID and password
    if user.id in users and users[user.id]['password'] == request.form['password']:
        login_user(user)
        logger.debug("Logged in successfully.")
        return redirect(url_for("auth_bp.protected"))

    logger.debug("Bad login.")
    return redirect(url_for("auth_bp.login"))


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
