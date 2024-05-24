from flask import Blueprint

# Adding _bp to the end of the instance name indicates a Flask Blueprint
intro_bp = Blueprint(
    'intro_bp', __name__,
    static_folder="static",  # relative to the file containing the definition of intro_bp
    # Ensure that the Blueprint relative path doesn't conflict with the root static folder
    static_url_path="/intro/static",  # relative to the root directory
    template_folder="templates",   # relative to the file containing the definition of intro_bp
)

# Run modules to define route functions
from . import home
from . import about
