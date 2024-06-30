from flask import Flask

from src.api.routes.assets import assets
from src.api.routes.user import user


def create_app():
    """
    Creates a Flask Application for the API
        Parameters:
            -
        Returns:
            Flask: The Flask Application
    """

    app = Flask(__name__, static_folder=None)

    # Register Blueprints
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(assets, url_prefix='/assets')

    return app
