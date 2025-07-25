import sys
import os
import uuid

# Ensure `backend/app/` is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))


import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user_model import Base, User
from services.user_service import UserService
from mappers.user_mapper import UserMapper

# Use SQLite in-memory DB for testing (isolated, fast, no data persistence)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def db_session():
    """
    Creates a new in-memory database for each test.
    """
    engine = create_engine(TEST_DATABASE_URL, echo=False)
    TestingSessionLocal = sessionmaker(bind=engine)
    # Create tables
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    yield session  # Provide the session to the test function
    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def mock_user_mapper(mocker):
    """
    Mocks the UserMapper methods to prevent real DB interactions.
    """
    return mocker.patch.object(UserMapper, "create_user")


def test_create_user(db_session, mock_user_mapper):
    """
    Test if `UserService.create_user()` correctly hashes passwords and creates users.
    """
    # Mock `UserMapper.create_user` to return a fake user.
    mock_user = User(
        user_id=1,
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password",
        age=25,
        gender="Male",
        fav_book="Dune",
        fav_author="Frank Herbert",
        preferred_genre="fiction",
    )
    mock_user_mapper.return_value = mock_user

    user = UserService.create_user(
        db_session,
        username="testuser",
        email="test@example.com",
        password="password123",
        age=25,
        gender="Male",
        fav_book="Dune",
        fav_author="Frank Herbert",
        preferred_genre="fiction"
    )

    assert user.username == "testuser"
    assert user.email == "test@example.com"
    assert user.age == 25
    assert user.gender == "Male"


def test_authenticate_user(db_session, mocker):
    """
    Test if `UserService.authenticate_user()` correctly verifies passwords.
    """
    from werkzeug.security import generate_password_hash

    hashed_password = generate_password_hash("securepassword", method="pbkdf2:sha256")
    test_user = User(
        username="testuser",
        email="test@example.com",
        password_hash=hashed_password,
        age=25,
        gender="Male",
        fav_book="Dune",
        fav_author="Frank Herbert",
        preferred_genre="fiction",
    )
    db_session.add(test_user)
    db_session.commit()

    # Patch the mapper so that it returns our test user.
    mocker.patch.object(UserMapper, "get_user_by_username_or_email", return_value=test_user)

    # Successful login.
    user = UserService.authenticate_user(db_session, "testuser", "securepassword")
    assert user is not None
    assert user.username == "testuser"

    # Wrong password should fail.
    user = UserService.authenticate_user(db_session, "testuser", "wrongpassword")
    assert user is None


def test_create_existing_user(db_session, mocker):
    """
    Test if `UserService.create_user()` handles duplicate users correctly.
    """
    from mappers.user_mapper import UserMapper
    from sqlalchemy.exc import IntegrityError

    # Add an existing user.
    existing_user = User(
        username="testuser",
        email="test@example.com",
        password_hash="hashed_password",
        age=25,
        gender="Male",
        fav_book="Dune",
        fav_author="Frank Herbert",
        preferred_genre="fiction",
    )
    db_session.add(existing_user)
    db_session.commit()

    # Patch the mapper so it returns the existing user.
    mocker.patch.object(UserMapper, "get_user_by_username_or_email", return_value=existing_user)

    with pytest.raises(IntegrityError):
        UserService.create_user(
            db_session,
            username="testuser",
            email="test@example.com",
            password="password123",
            age=25,
            gender="Male",
            fav_book="Dune",
            fav_author="Frank Herbert",
            preferred_genre="fiction"
        )

def generate_unique(prefix):
    """Generate a unique string using a short UUID suffix."""
    return f"{prefix}_{uuid.uuid4().hex[:6]}"

def test_get_user_by_id(db_session):
    """
    Test if `UserService.get_user_by_id()` correctly retrieves a user by its ID.
    """
    unique_username = generate_unique("getuser")
    unique_email = f"{unique_username}@example.com"
    # Create a new user.
    user = UserService.create_user(
        db_session,
        username=unique_username,
        email=unique_email,
        password="pass",
        age=30,
        gender="Male",
        fav_book="Some Book",
        fav_author="Some Author",
        preferred_genre="fiction"
    )
    # Retrieve the user using the service.
    fetched_user = UserService.get_user_by_id(db_session, user.user_id)
    assert fetched_user is not None
    assert fetched_user.user_id == user.user_id


def test_update_user_profile(db_session):
    """
    Test if `UserService.update_user_profile()` correctly updates user data.
    Also checks that camelCase API fields map correctly to snake_case DB fields.
    """
    unique_username = generate_unique("updateprofile")
    unique_email = f"{unique_username}@example.com"
    # Create a new user.
    user = UserService.create_user(
        db_session,
        username=unique_username,
        email=unique_email,
        password="pass",
        age=30,
        gender="Male",
        fav_book="Old Book",
        fav_author="Old Author",
        preferred_genre="fiction"
    )
    # Define the update data.
    update_data = {
        "username": "newusername",
        "email": "newemail@example.com",
        "age": 35,
        "gender": "Male",
        "favoriteBook": "New Book",
        "favoriteAuthor": "New Author",
        "preferredGenre": "fiction"
    }
    updated_user = UserService.update_user_profile(db_session, user.user_id, update_data)
    assert updated_user is not None
    assert updated_user.username == "newusername"
    assert updated_user.email == "newemail@example.com"
    assert updated_user.age == 35
    # Verify mapping: API field favoriteBook to DB field fav_book.
    assert updated_user.fav_book == "New Book"
    assert updated_user.fav_author == "New Author"

    # Test updating a non-existent user returns None.
    assert UserService.update_user_profile(db_session, 999999, update_data) is None


def test_delete_user(db_session):
    """
    Test if `UserService.delete_user()` correctly deletes a user.
    """
    unique_username = generate_unique("deluser")
    unique_email = f"{unique_username}@example.com"
    # Create a new user.
    user = UserService.create_user(
        db_session,
        username=unique_username,
        email=unique_email,
        password="pass",
        age=30,
        gender="Male",
        fav_book="Book",
        fav_author="Author",
        preferred_genre="fiction"
    )
    # Delete the user.
    result = UserService.delete_user(db_session, user.user_id)
    assert result is True
    # Verify that fetching the deleted user returns None.
    assert UserService.get_user_by_id(db_session, user.user_id) is None

    # Attempt to delete a non-existent user.
    assert UserService.delete_user(db_session, 999999) is False


def test_logout_user(db_session):
    """
    Test if `UserService.logout_user()` returns True when a user exists,
    and False when the user does not exist.
    """
    unique_username = generate_unique("logoutuser")
    unique_email = f"{unique_username}@example.com"
    # Create a user.
    UserService.create_user(
        db_session,
        username=unique_username,
        email=unique_email,
        password="pass",
        age=30,
        gender="Male",
        fav_book="Book",
        fav_author="Author",
        preferred_genre="fiction"
    )
    result = UserService.logout_user(db_session, unique_username)
    assert result is True

    # Test logout for a non-existent user.
    result = UserService.logout_user(db_session, "nonexistentuser")
    assert result is False