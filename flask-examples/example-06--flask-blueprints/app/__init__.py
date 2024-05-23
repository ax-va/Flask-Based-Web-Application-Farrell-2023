from flask import Flask


def create_app():
    """ Application factory creating the Flask app instance """
    app = Flask(__name__)
    with app.app_context():
        from . import intro  # Import the package "intro" that imports the module "intro"
        # Register intro.intro_bp with app
        app.register_blueprint(intro.intro_bp)

    return app
