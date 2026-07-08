from pathlib import Path

from flask import Flask
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge

from .api.files import files_blueprint
from .api.health import health_blueprint
from .api.tasks import tasks_blueprint
from .config import Config, PROJECT_ROOT
from .extensions import db, migrate
from .utils.responses import error_response


def create_app(config_object: type[Config] = Config) -> Flask:
    """Create and configure a Flask application instance."""
    app = Flask(__name__, instance_path=str(PROJECT_ROOT / "instance"))
    app.config.from_object(config_object)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    (Path(app.config["UPLOAD_ROOT"]) / "original").mkdir(parents=True, exist_ok=True)

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})
    db.init_app(app)
    migrate.init_app(app, db)

    from .models import AnalysisTask, TaskInputFile, TaskResult, UploadedFile  # noqa: F401

    app.register_blueprint(files_blueprint, url_prefix="/api/v1")
    app.register_blueprint(health_blueprint, url_prefix="/api/v1")
    app.register_blueprint(tasks_blueprint, url_prefix="/api/v1")

    @app.errorhandler(RequestEntityTooLarge)
    def handle_file_too_large(error):
        return error_response(
            code="FILE_TOO_LARGE",
            message=f"请求体超过 {app.config['MAX_UPLOAD_MB']} MB 限制",
            status_code=413,
        )

    return app
