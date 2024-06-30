from flask import Flask

from src.routes.user import user
from src.routes.assets import assets


def create_app():
    """
    Creates a Flask Application for the API
        Parameters:
            -
        Returns:
            Flask: The Flask Application
    """

    app = Flask(__name__)

    # Register Blueprints
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(assets, url_prefix='/assets')

    return app