import pytest
from main import app
from application.data.database import db

@pytest.fixture(scope="module")
def client():
    # Arrange
    client = app.test_client()
    ctx = app.app_context()
    ctx.push()

    # Act
    yield client

    # Cleanup
    ctx.pop()

@pytest.fixture(scope="module")
def init_database():
    db.create_all()

    yield db

    db.drop_all()