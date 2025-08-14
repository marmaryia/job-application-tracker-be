import pytest

from lib.db.seed import seed
from extensions import db
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

    yield app.test_client()

def test_register_success(app):
    """
    Accepts a request body with name, email and password and returns the newly created user as JSON.
    """
    response = app.post("api/auth/register", json={"name": "Test Name", "email": "test@email.com", "password": "11111111"})
    assert response.status_code == 201
    assert response.json["user"] == {"name": "Test Name", "email": "test@email.com", "id": 4}

def test_register_duplicate_email(app):
    """
    Returns a 400 error if a user with the email provided already exists in the database.
    """
    response = app.post("api/auth/register", json={"name": "Test Name", "email": "user1@email.com", "password": "11111111"})
    assert response.status_code == 400
    assert response.json == {"error": "DUPLICATE_RESOURCE", "message": "This resource already exists"}

def test_register_incomplete_data(app):
    """
    Returns a 400 error if an incomplete data object is provided.
    """
    response = app.post("api/auth/register", json={"name": "Test Name", "password": "11111111"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request"}

    response = app.post("api/auth/register", json={"email": "user123@email.com", "password": "11111111"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request"}

    response = app.post("api/auth/register", json={"name": "Test Name", "email": "user123@email.com", })
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request"}

def test_register_incomplete_data(app):
    """
    Returns a 400 error if a data object with invalid data is provided.
    """
    response = app.post("api/auth/register", json={"name": "", "email": "user123@email.com", "password": "11111111"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request: Invalid Input"}

    response = app.post("api/auth/register", json={"name": "name", "email": "user123", "password": "11111111"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request: Invalid Input"}

    response = app.post("api/auth/register", json={"name": "name", "email": "", "password": "11111111"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request: Invalid Input"}

    response = app.post("api/auth/register", json={"name": "name", "email": "user123@email.com", "password": ""})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request: Invalid Input"}

    response = app.post("api/auth/register", json={"name": "name", "email": "user123@email.com", "password": "1234567"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request: Invalid Input"}

    response = app.post("api/auth/register", json={"name": "name", "email": "user123@email.com", "password": "12 34567"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request: Invalid Input"}