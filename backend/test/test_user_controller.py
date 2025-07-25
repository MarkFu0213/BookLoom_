import sys
import os
import uuid

# Ensure "backend/app/" is in sys.path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

import pytest
import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Set the environment variable to force using an in-memory database.
os.environ["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
TEST_DATABASE_URL = "sqlite:///:memory:"

# Import create_app from your main application. (Assumes main.py lives under app/)
from main import create_app

# Import models, services, and mappers.
from models.user_model import Base, User
from services.user_service import UserService
from mappers.user_mapper import UserMapper


###########################################
# Utility to generate unique usernames/emails.
###########################################
def generate_unique(prefix):
    # Create a short unique suffix.
    suffix = uuid.uuid4().hex[:6]
    return f"{prefix}_{suffix}"


###########################################
# db_session Fixture (for direct service-level tests)
###########################################
@pytest.fixture(scope="function")
def db_session():
    """
    Creates a fresh in-memory database session for each test.
    """
    engine = create_engine(TEST_DATABASE_URL, echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


###########################################
# App and Client Fixtures (for controller tests)
###########################################
@pytest.fixture
def app():
    app = create_app()
    # Override configuration for testing.
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    return app

@pytest.fixture
def client(app):
    return app.test_client()


###########################################
# Controller Tests
###########################################
def test_register(client):
    unique_username = generate_unique("newuser")
    unique_email = f"{unique_username}@example.com"
    data = {
        "username": unique_username,
        "email": unique_email,
        "password": "password123",
        "age": 30,
        "gender": "Male",
        "favoriteBook": "Test Book",
        "favoriteAuthor": "Author One",
        "preferredGenre": "fiction"
    }
    response = client.post("/auth/register", json=data)
    assert response.status_code == 201, response.get_data(as_text=True)
    json_data = response.get_json()
    assert "userId" in json_data
    assert json_data["message"] == "User registered successfully"


def test_login(client):
    unique_username = generate_unique("loginuser")
    unique_email = f"{unique_username}@example.com"
    # Register a user first.
    reg_data = {
        "username": unique_username,
        "email": unique_email,
        "password": "password456",
        "age": 28,
        "gender": "Female",
        "favoriteBook": "Test Book",
        "favoriteAuthor": "Author Two",
        "preferredGenre": "fiction"
    }
    client.post("/auth/register", json=reg_data)

    # Login with the same credentials.
    login_data = {"username": unique_username, "password": "password456"}
    response = client.post("/auth/login", json=login_data)
    assert response.status_code == 200, response.get_data(as_text=True)
    json_data = response.get_json()
    assert json_data.get("userId") is not None
    assert json_data["email"] == unique_email


def test_get_user_profile(client):
    unique_username = generate_unique("profileuser")
    unique_email = f"{unique_username}@example.com"
    # Register a user.
    reg_data = {
        "username": unique_username,
        "email": unique_email,
        "password": "password789",
        "age": 22,
        "gender": "Male",
        "favoriteBook": "Test Book",
        "favoriteAuthor": "Author Three",
        "preferredGenre": "fiction"
    }
    reg_resp = client.post("/auth/register", json=reg_data)
    # Ensure registration succeeded.
    assert reg_resp.status_code == 201, reg_resp.get_data(as_text=True)
    json_reg = reg_resp.get_json()
    assert "userId" in json_reg
    user_id = json_reg["userId"]

    # Get the user profile.
    response = client.get(f"/users/{user_id}/profile")
    assert response.status_code == 200, response.get_data(as_text=True)
    profile = response.get_json()
    assert profile["username"] == unique_username


def test_update_profile(client):
    unique_username = generate_unique("updateuser")
    unique_email = f"{unique_username}@example.com"
    # Register a user.
    reg_data = {
        "username": unique_username,
        "email": unique_email,
        "password": "passwordupd",
        "age": 35,
        "gender": "Female",
        "favoriteBook": "Initial Book",
        "favoriteAuthor": "Initial Author",
        "preferredGenre": "fiction"
    }
    reg_resp = client.post("/auth/register", json=reg_data)
    assert reg_resp.status_code == 201, reg_resp.get_data(as_text=True)
    json_reg = reg_resp.get_json()
    assert "userId" in json_reg
    user_id = json_reg["userId"]

    update_data = {"favoriteBook": "Updated Book", "favoriteAuthor": "Updated Author"}
    response = client.put(f"/users/{user_id}/profile", json=update_data)
    assert response.status_code == 200, response.get_data(as_text=True)
    updated_profile = response.get_json()["updatedProfile"]
    assert updated_profile["favoriteBook"] == "Updated Book"
    assert updated_profile["favoriteAuthor"] == "Updated Author"


def test_delete_user(client):
    unique_username = generate_unique("deleteuser")
    unique_email = f"{unique_username}@example.com"
    # Register a user.
    reg_data = {
        "username": unique_username,
        "email": unique_email,
        "password": "passworddel",
        "age": 40,
        "gender": "Male",
        "favoriteBook": "Book To Delete",
        "favoriteAuthor": "Author Four",
        "preferredGenre": "fiction"
    }
    reg_resp = client.post("/auth/register", json=reg_data)
    assert reg_resp.status_code == 201, reg_resp.get_data(as_text=True)
    json_reg = reg_resp.get_json()
    assert "userId" in json_reg
    user_id = json_reg["userId"]

    # Delete the user.
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200, response.get_data(as_text=True)
    json_data = response.get_json()
    assert json_data["message"] == "User deleted successfully"


def test_logout(client):
    unique_username = generate_unique("logoutuser")
    unique_email = f"{unique_username}@example.com"
    # Register a user.
    reg_data = {
        "username": unique_username,
        "email": unique_email,
        "password": "passwordlogout",
        "age": 29,
        "gender": "Female",
        "favoriteBook": "Some Book",
        "favoriteAuthor": "Author Five",
        "preferredGenre": "fiction"
    }
    reg_resp = client.post("/auth/register", json=reg_data)
    assert reg_resp.status_code == 201, reg_resp.get_data(as_text=True)

    # Logout the user.
    response = client.post("/auth/logout", json={"username": unique_username})
    assert response.status_code == 200, response.get_data(as_text=True)
    logout_resp = response.get_json()
    assert logout_resp["message"] == "User logged out"

def test_duplicate_registration(client):
    """
    Attempt to register a user with the same username and email twice.
    The second registration should return an error status and a clear error message.
    """
    unique_username = generate_unique("dupuser")
    unique_email = f"{unique_username}@example.com"
    data = {
        "username": unique_username,
        "email": unique_email,
        "password": "passworddup",
        "age": 30,
        "gender": "Male",
        "favoriteBook": "Test Book",
        "favoriteAuthor": "Author Dup",
        "preferredGenre": "fiction"
    }
    # First registration should succeed.
    response1 = client.post("/auth/register", json=data)
    assert response1.status_code == 201, response1.get_data(as_text=True)

    # Second registration with same data should fail.
    response2 = client.post("/auth/register", json=data)
    # Depending on your implementation, this might be a 500 or custom error code.
    # Adjust the expected status and message accordingly.
    assert response2.status_code in [400, 500]
    json_data = response2.get_json()
    # Check that the error message mentions duplicate entry.
    assert "duplicate" in json_data.get("error", "").lower() or "exists" in json_data.get("error", "").lower()


def test_register_invalid_data_formats(client):
    """
    Test registration with invalid data formats:
    - Email is not valid.
    - Age is a string instead of an integer.
    - Gender is an unsupported value.
    The endpoint should return a 500 error with appropriate error messages.
    """
    unique_username = generate_unique("invaliduser")
    data = {
        "username": unique_username,
        "email": "not-an-email",  # invalid email
        "password": "passwordinvalid",
        "age": "twenty",         # non-integer age
        "gender": "Unknown",     # unsupported gender value
        "favoriteBook": "Test Book",
        "favoriteAuthor": "Author Invalid",
        "preferredGenre": "fiction"
    }
    response = client.post("/auth/register", json=data)
    # Expected to be a 500 Error
    assert response.status_code == 500, response.get_data(as_text=True)
    json_data = response.get_json()
    # Check that error messages indicate the invalid fields.
    error_msg = json_data.get("error", "").lower()
    assert "email" in error_msg
    assert "age" in error_msg
    assert "gender" in error_msg


def test_update_profile_no_valid_fields(client):
    """
    Send an update request with no valid fields.
    The endpoint should return an error indicating no valid fields were provided.
    """
    unique_username = generate_unique("novalidupdate")
    unique_email = f"{unique_username}@example.com"
    reg_data = {
        "username": unique_username,
        "email": unique_email,
        "password": "passwordnovalid",
        "age": 32,
        "gender": "Male",
        "favoriteBook": "Initial Book",
        "favoriteAuthor": "Initial Author",
        "preferredGenre": "fiction"
    }
    reg_resp = client.post("/auth/register", json=reg_data)
    user_id = reg_resp.get_json()["userId"]

    # Send update with an empty JSON payload.
    response = client.put(f"/users/{user_id}/profile", json={})
    assert response.status_code == 400, response.get_data(as_text=True)
    json_data = response.get_json()
    # Check that error message indicates missing valid update fields.
    assert "no valid" in json_data.get("error", "").lower()


def test_delete_nonexistent_user(client):
    """
    Try to delete a user that doesn't exist.
    The endpoint should return a 404 error with a "User not found" message.
    """
    response = client.delete("/users/999999")  # Assuming 999999 is a non-existent user ID.
    assert response.status_code == 404, response.get_data(as_text=True)
    json_data = response.get_json()
    assert "not found" in json_data.get("error", "").lower()


def test_logout_nonexistent_user(client):
    """
    Attempt to log out a user that does not exist.
    The endpoint should return an error (likely 404) with an appropriate message.
    """
    response = client.post("/auth/logout", json={"username": "nonexistentuser"})
    # Adjust expected status code based on your implementation.
    assert response.status_code in [404, 400]
    json_data = response.get_json()
    assert "not found" in json_data.get("error", "").lower() or "does not exist" in json_data.get("error", "").lower()


# -----------------------
# Register: missing field
# -----------------------
def test_register_missing_field(client):
    # Drop the "email" field
    data = {
        "username": "user1",
        "password": "pass",
        "age": 20,
        "gender": "Male",
        "favoriteBook": "B",
        "favoriteAuthor": "A",
        "preferredGenre": "fiction"
    }
    resp = client.post("/auth/register", json=data)
    assert resp.status_code == 400
    body = resp.get_json()
    assert "Missing field: email" in body["error"]

# -------------------------------------------
# Register: service raises ValueError → 400
# -------------------------------------------
def test_register_service_validation_error(client, mocker):
    data = {
        "username": "user2",
        "email": "u2@example.com",
        "password": "pass",
        "age": 20,
        "gender": "Male",
        "favoriteBook": "B",
        "favoriteAuthor": "A",
        "preferredGenre": "fiction"
    }
    mocker.patch.object(UserService, "create_user", side_effect=ValueError("bad business"))
    resp = client.post("/auth/register", json=data)
    assert resp.status_code == 400
    assert "bad business" in resp.get_json()["error"]

# --------------------------------------
# Login: service throws exception → 500
# --------------------------------------
def test_login_service_exception(client, mocker):
    mocker.patch.object(UserService, "authenticate_user", side_effect=Exception("db down"))
    resp = client.post("/auth/login", json={"username":"u","password":"p"})
    assert resp.status_code == 500
    assert "db down" in resp.get_json()["error"]

# -------------------------------
# GET profile: user not found → 404
# -------------------------------
def test_get_user_profile_not_found(client):
    resp = client.get("/users/9999/profile")
    assert resp.status_code == 404
    assert "not found" in resp.get_json()["error"].lower()

# ---------------------------------------
# GET profile: service exception → 500
# ---------------------------------------
def test_get_profile_service_exception(client, mocker):
    mocker.patch.object(UserService, "get_user_by_id", side_effect=Exception("oops"))
    resp = client.get("/users/1/profile")
    assert resp.status_code == 500
    assert "oops" in resp.get_json()["error"]

# --------------------------------------
# UPDATE profile: user not found → 404
# --------------------------------------
def test_update_profile_user_not_found(client, mocker):
    mocker.patch.object(UserService, "update_user_profile", return_value=None)
    data = {"username": "foo"}
    resp = client.put("/users/9999/profile", json=data)
    assert resp.status_code == 404
    assert "not found" in resp.get_json()["error"].lower()

# ----------------------------------------
# UPDATE profile: service exception → 500
# ----------------------------------------
def test_update_profile_service_exception(client, mocker):
    mocker.patch.object(UserService, "update_user_profile", side_effect=Exception("fail"))
    resp = client.put("/users/1/profile", json={"username":"x"})
    assert resp.status_code == 500
    assert "fail" in resp.get_json()["error"]

# --------------------------------------------
# DELETE user: service exception → 500
# --------------------------------------------
def test_delete_user_service_exception(client, mocker):
    mocker.patch.object(UserService, "delete_user", side_effect=Exception("gone"))
    resp = client.delete("/users/1")
    assert resp.status_code == 500
    assert "gone" in resp.get_json()["error"]

# ----------------------------------------
# LOGOUT: missing username → 400
# ----------------------------------------
def test_logout_missing_username(client):
    resp = client.post("/auth/logout", json={})
    assert resp.status_code == 400
    assert "required" in resp.get_json()["error"].lower()

# ------------------------------------------
# LOGOUT: service exception → 500
# ------------------------------------------
def test_logout_service_exception(client, mocker):
    mocker.patch.object(UserService, "logout_user", side_effect=Exception("timeout"))
    resp = client.post("/auth/logout", json={"username": "u"})
    assert resp.status_code == 500
    assert "timeout" in resp.get_json()["error"]

# --------------------------------------
# Register: service throws generic error → 500
# --------------------------------------
def test_register_service_exception(client, mocker):
    # Prepare a perfectly valid payload
    payload = {
        "username": "erruser",
        "email": "erruser@example.com",
        "password": "pass123",
        "age": 25,
        "gender": "Male",
        "favoriteBook": "Some Book",
        "favoriteAuthor": "Some Author",
        "preferredGenre": "fiction"
    }
    # Have the service layer blow up with a generic Exception
    mocker.patch.object(UserService, "create_user", side_effect=Exception("db down"))
    resp = client.post("/auth/register", json=payload)
    assert resp.status_code == 500
    assert "db down" in resp.get_json()["error"]

def test_login_invalid_credentials(client):
    # 1) Register a valid user
    unique_username = generate_unique("wrongpass")
    unique_email = f"{unique_username}@example.com"
    client.post("/auth/register", json={
        "username": unique_username,
        "email": unique_email,
        "password": "rightpass",
        "age": 30,
        "gender": "Male",
        "favoriteBook": "Test",
        "favoriteAuthor": "Author",
        "preferredGenre": "fiction"
    })

    # 2) Attempt to login with the wrong password
    resp = client.post("/auth/login", json={
        "username": unique_username,
        "password": "wrongpass"
    })
    assert resp.status_code == 401
    body = resp.get_json()
    assert body["error"].lower() == "invalid username or password"

# --------------------------------------
# Login: missing username/password → 400
# --------------------------------------
@pytest.mark.parametrize("body", [None, {}, {"username":"u"}, {"password":"p"}])
def test_login_missing_credentials(client, body):
    if body is None:
        # send an empty JSON body with the correct content type
        resp = client.post(
            "/auth/login",
            data="",
            content_type="application/json"
        )
    else:
        resp = client.post("/auth/login", json=body)

    assert resp.status_code == 400