from datetime import datetime
from logging import getLogger

from flask import render_template
from flask_login import login_required

from . import intro_bp
from .cls.banner_colors import BannerColors
from .cls.page_visit import PageVisit

logger = getLogger(__file__)


@intro_bp.route("/")
@login_required
def home():
    logger.debug("Rendering the 'home' page...")
    return render_template(
        "index.html",
        data={
            "now": datetime.now(),
            "page_visit": PageVisit(),
            "banner_colors": BannerColors.get_colors(),
        }
    )
