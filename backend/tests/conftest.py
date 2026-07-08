import pytest

from app import create_app
from app.config import Config
from app.extensions import db


class TestConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"


@pytest.fixture()
def app(tmp_path):
    TestConfig.UPLOAD_ROOT = str(tmp_path / "uploads")
    TestConfig.MAX_UPLOAD_MB = 1
    TestConfig.MAX_CONTENT_LENGTH = 1024 * 1024
    TestConfig.MAX_IMAGE_PIXELS = 1_000_000
    application = create_app(TestConfig)
    with application.app_context():
        db.create_all()

    yield application

    with application.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
