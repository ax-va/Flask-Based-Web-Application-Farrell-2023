import os
from flask import Flask
from dynaconf import FlaskDynaconf


def create_app() -> Flask:
    """ This application factory creates the Flask app instance with the application context """
    app = Flask(__name__)
    dynaconf = FlaskDynaconf(extensions_list=True)
    with app.app_context():
        # Inform dynaconf where to look for configuration *.toml files
        os.environ["ROOT_PATH_FOR_DYNACONF"] = app.root_path
        # Configure the Flask app based on the dynaconf-read configuration files
        dynaconf.init_app(app)
        # Import the "intro" package, which contains the "intro_bp" instance
        from . import intro
        # Register intro.intro_bp with app
        app.register_blueprint(intro.intro_bp)

    return app
