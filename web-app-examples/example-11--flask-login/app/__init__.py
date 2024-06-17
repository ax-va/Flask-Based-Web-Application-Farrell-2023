import logging
import logging.config
import os
import yaml
from pathlib import Path
from dynaconf import FlaskDynaconf
from flask import Flask, send_from_directory
from flask_login import LoginManager  # to handle user authentication

# Create an uninitialized LoginManager instance
login_manager = LoginManager()
# Point the LoginManager instance to the Blueprint view
login_manager.login_view = "auth_bp.login"

# Mock database
users_db = {'ax-va@email.com': {'password': 'secret'}}


def create_app() -> Flask:
    """ This application factory creates the Flask app instance with the application context """
    app = Flask(__name__)
    dynaconf = FlaskDynaconf(extensions_list=True)

    with app.app_context():
        # Create a route to the favicon.ico file
        @app.route('/favicon.ico')
        def favicon():
            return send_from_directory(
                os.path.join(app.root_path, 'static', 'images'),
                'favicon.ico',
                mimetype="image/vnd.microsoft.icon"
            )
        # Inform dynaconf where to look for configuration *.toml files
        os.environ["ROOT_PATH_FOR_DYNACONF"] = app.root_path
        # Configure the Flask app based on the dynaconf-read configuration files
        dynaconf.init_app(app)
        # Initialize the login manager
        login_manager.init_app(app)
        # Configure logging for the application
        _configure_logging(app, dynaconf)

        # Import the routes
        from . import intro
        from . import auth

        # Register the blueprints
        app.register_blueprint(intro.intro_bp)
        app.register_blueprint(auth.auth_bp)

    return app


def _configure_logging(app, dynaconf):
    """ Configure logging """
    logging_config_path = Path(app.root_path).parent / "logging_config.yaml"
    with open(logging_config_path, "r") as fh:
        logging_config = yaml.safe_load(fh.read())
    env_logging_level = dynaconf.settings.get("logging_level", "INFO").upper()
    logging_level = logging.INFO if env_logging_level == "INFO" else logging.DEBUG
    logging_config["handlers"]["console"]["level"] = logging_level
    logging_config["loggers"][""]["level"] = logging_level
    logging.config.dictConfig(logging_config)
