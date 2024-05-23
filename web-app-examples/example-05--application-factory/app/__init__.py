from datetime import datetime
from flask import Flask, render_template
from .banner_colors import BannerColors
from .page_visit import PageVisit


def create_app():
    """ Application factory creating the Flask app instance """

    app = Flask(__name__)

    # Initialize the rest of the app
    with app.app_context():
        @app.route("/")
        def home():
            return render_template(
                "index.html",
                data={
                    "now": datetime.now(),
                    "page_visit": PageVisit(),
                    "banner_colors": BannerColors.get_colors(),
                }
            )

    return app
