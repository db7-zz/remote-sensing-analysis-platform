from datetime import UTC, datetime

from flask import Blueprint

from app.utils.responses import success_response


health_blueprint = Blueprint("health", __name__)


@health_blueprint.get("/health")
def health_check():
    return success_response(
        data={
            "service": "remote-sensing-api",
            "status": "healthy",
            "version": "0.1.0",
            "timestamp": datetime.now(UTC).isoformat(),
        },
        message="API service is healthy",
    )

