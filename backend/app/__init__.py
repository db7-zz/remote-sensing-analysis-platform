from pathlib import Path

from flask import Flask
from flask_cors import CORS

from .api.health import health_blueprint
from .api.tasks import tasks_blueprint
from .config import Config, PROJECT_ROOT
from .extensions import db, migrate


def create_app(config_object: type[Config] = Config) -> Flask:
    """Create and configure a Flask application instance."""
    app = Flask(__name__, instance_path=str(PROJECT_ROOT / "instance"))
    app.config.from_object(config_object)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    db.init_app(app)
    migrate.init_app(app, db)

    from .models.analysis_task import AnalysisTask  # noqa: F401

    app.register_blueprint(health_blueprint, url_prefix="/api/v1")
    app.register_blueprint(tasks_blueprint, url_prefix="/api/v1")

    return app
