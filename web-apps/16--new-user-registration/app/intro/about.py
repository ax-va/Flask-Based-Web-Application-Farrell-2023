from logging import getLogger

from flask import render_template
from flask_login import login_required

from . import intro_bp

logger = getLogger(__file__)


@intro_bp.route("/about")
@login_required
def about():
    logger.debug("Rendering the 'about' page...")
    return render_template("about.html")
