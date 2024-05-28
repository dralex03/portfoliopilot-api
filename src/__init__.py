from flask import Flask

from src.routes.user import user

api = Flask(__name__)

# Register Blueprints
api.register_blueprint(user, url_prefix='/user')