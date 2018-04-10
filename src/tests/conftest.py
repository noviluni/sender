import pytest
from api import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object('api.config.TestingConfig')
    return app