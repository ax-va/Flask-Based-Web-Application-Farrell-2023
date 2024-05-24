from flask import render_template
from . import intro_bp


@intro_bp.route("/about")
def about():
    return render_template("about.html")
