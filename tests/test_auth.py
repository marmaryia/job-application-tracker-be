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

def test_register_success(client):
    """
    Accepts a request body with name, email and password and returns the newly created user as JSON.
    """
    response = client.post("api/auth/register", json={"name": "Test Name", "email": "test@email.com", "password": "11111111"})
    assert response.status_code == 201
    assert response.json["user"] == {"name": "Test Name", "email": "test@email.com", "id": 4}

def test_register_duplicate_email(client):
    """
    Returns a 400 error if a user with the email provided already exists in the database.
    """
    response = client.post("api/auth/register", json={"name": "Test Name", "email": "user1@email.com", "password": "11111111"})
    assert response.status_code == 400
    assert response.json == {"error": "DUPLICATE_RESOURCE", "message": "This resource already exists"}

def test_register_incomplete_data(client):
    """
    Returns a 400 error if an incomplete data object is provided.
    """
    response = client.post("api/auth/register", json={"name": "Test Name", "password": "11111111"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request"}

    response = client.post("api/auth/register", json={"email": "user123@email.com", "password": "11111111"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request"}

    response = client.post("api/auth/register", json={"name": "Test Name", "email": "user123@email.com", })
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request"}

def test_register_invalid_data(client):
    """
    Returns a 400 error if a data object with invalid data is provided.
    """
    response = client.post("api/auth/register", json={"name": "", "email": "user123@email.com", "password": "11111111"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request: Invalid Input"}

    response = client.post("api/auth/register", json={"name": "name", "email": "user123", "password": "11111111"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request: Invalid Input"}

    response = client.post("api/auth/register", json={"name": "name", "email": "", "password": "11111111"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request: Invalid Input"}

    response = client.post("api/auth/register", json={"name": "name", "email": "user123@email.com", "password": ""})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request: Invalid Input"}

    response = client.post("api/auth/register", json={"name": "name", "email": "user123@email.com", "password": "1234567"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request: Invalid Input"}

    response = client.post("api/auth/register", json={"name": "name", "email": "user123@email.com", "password": "12 34567"})
    assert response.status_code == 400
    assert response.json == {"message": "Bad Request: Invalid Input"}

def test_login_success(client, mocker):
    """
    Accepts a request body with email and password and returns a JSON object with the logged in user and the access token.
    """
    mocked_token_creator = mocker.patch("lib.api.controllers.auth.create_access_token", return_value = "access_token")
    
    response = client.post("api/auth/login", json={"email": "user1@email.com", "password": "123456"})
    assert response.status_code == 200
    assert response.json["user"] == {"name": "user1", "email": "user1@email.com", "id": 1}
    assert response.json["access_token"] == "access_token"
    mocked_token_creator.assert_called_once()

def test_login_incorrect_password(client):
    """
    Returns an authentication 401 error if the password provided is incorrect. 
    """
    response = client.post("api/auth/login", json={"email": "user1@email.com", "password": "12345678"})
    assert response.status_code == 401
    assert response.json["message"] == "Authentication Failed"
    
def test_login_nonexistent_user(client):
    """
    Returns a 404 error if no user with the provided email address. 
    """
    response = client.post("api/auth/login", json={"email": "user123@email.com", "password": "123456"})
    assert response.status_code == 404
    assert response.json["message"] == "Resource not found"

def test_login_incomplete_data(client):
    """
    Returns a 400 error if the data object provided is incomplete. 
    """
    response = client.post("api/auth/login", json={"password": "123456"})
    assert response.status_code == 400
    assert response.json["message"] == "Bad Request"

    response = client.post("api/auth/login", json={"email": "user1@email.com"})
    assert response.status_code == 400
    assert response.json["message"] == "Bad Request"

def test_login_invalid_data(client):
    """
    Returns a 400 error if the data object provided is invalid. 
    """
    response = client.post("api/auth/login", json={"email": "user1@email.com", "password": ""})
    assert response.status_code == 400
    assert response.json["message"] == "Bad Request"

    response = client.post("api/auth/login", json={"email": "", "password": "123456"})
    assert response.status_code == 400
    assert response.json["message"] == "Bad Request"

def test_logout_success(client, auth_header):
    """
    Returns a message if successfully logged out
    """
   
    response = client.delete("api/auth/logout", headers=auth_header)
    assert response.status_code == 200
    assert response.json["message"] == "Logged out successfully"

    response = client.delete("api/auth/logout", headers=auth_header)
    assert response.status_code == 401
    