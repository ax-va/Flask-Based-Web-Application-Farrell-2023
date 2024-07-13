from flask import Flask


def create_app() -> Flask:
    """ This application factory creates the Flask app instance with the application context """
    app = Flask(__name__)
    with app.app_context():
        # Import the "intro" package, which contains the "intro_bp" instance
        from . import intro
        # Register intro.intro_bp with app
        app.register_blueprint(intro.intro_bp)

    return app