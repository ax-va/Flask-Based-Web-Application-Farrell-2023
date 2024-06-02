from logging import getLogger

from flask import render_template
from . import intro_bp

logger = getLogger(__file__)


@intro_bp.route("/about")
def about():
    logger.debug("Rendering the 'about' page...")
    return render_template("about.html")
