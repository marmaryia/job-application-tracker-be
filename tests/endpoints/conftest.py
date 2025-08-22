import pytest

from lib.db.seed import seed
from lib.db.data import users, applications, events
from app import create_app

@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        seed(users, applications, events)

    yield app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def auth_header(app):

    class Dummy:
        def __init__(self, id):
            self.id = id 
    dummy_user = Dummy(1)
    from flask_jwt_extended import create_access_token
    with app.app_context():
        token = create_access_token(identity=dummy_user)
    return {"Authorization": f"Bearer {token}"}