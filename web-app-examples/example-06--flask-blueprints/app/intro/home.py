from datetime import datetime
from flask import render_template
from . import intro_bp
from .cls.banner_colors import BannerColors
from .cls.page_visit import PageVisit


@intro_bp.route("/")
def home():
    return render_template(
        "index.html",
        data={
            "now": datetime.now(),
            "page_visit": PageVisit(),
            "banner_colors": BannerColors.get_colors(),
        }
    )
