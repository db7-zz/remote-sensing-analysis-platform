from flask import Flask
from flask_cors import CORS

from .api.health import health_blueprint
from .config import Config


def create_app(config_object: type[Config] = Config) -> Flask:
    """Create and configure a Flask application instance."""
    app = Flask(__name__)
    app.config.from_object(config_object)

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    app.register_blueprint(health_blueprint, url_prefix="/api/v1")

    return app

