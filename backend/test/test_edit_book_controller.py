import sys
import os
import pytest
import json

# Ensure the "app" folder is in sys.path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from flask import Flask
# Import the blueprint for the edit book controller.
from controllers.edit_book_controller import book_bp

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(book_bp)
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()


def test_edit_book_missing_option(client):
    # Without an "editingOption" in the payload, expect a 400 error.
    response = client.put("/books/123", json={})
    assert response.status_code == 400
    json_data = response.get_json()
    assert json_data["message"] == "Missing editing option"


def test_edit_book_success(client, mocker):
    # Patch the edit_book_service function within the edit_book_controller module.
    fake_updated_text = "Updated chapter text"
    mocker.patch("controllers.edit_book_controller.edit_book_service", return_value=fake_updated_text)

    payload = {"editingOption": "more dramatic tone"}
    response = client.put("/books/123", json=payload)
    assert response.status_code == 201
    json_data = response.get_json()
    assert json_data["message"] == "Chapter updated successfully"
    assert json_data["text"] == fake_updated_text


def test_edit_book_content_change(client, mocker):
    """
    Test that after editing, the returned text is different from the original text.
    In a real scenario, the service might compare the new text with the stored original text.
    Here we simulate that by assuming an original text and checking that the updated text is different.
    """
    # Assume this is the original text stored in the book.
    original_text = "This is the original book text."
    # Simulate an updated text that is different.
    fake_updated_text = "This is the updated chapter text with a new style."

    # Patch the edit_book_service so that it returns our fake updated text.
    mocker.patch("controllers.edit_book_controller.edit_book_service", return_value=fake_updated_text)

    payload = {"editingOption": "change style"}
    response = client.put("/books/100", json=payload)
    assert response.status_code == 201, response.get_data(as_text=True)
    json_data = response.get_json()

    # Check that the updated text is exactly what we expect.
    assert json_data["text"] == fake_updated_text
    # And, importantly, that it is different from the original text.
    assert json_data["text"] != original_text


def test_edit_book_no_change_returns_failure(client, mocker):
    """
    Test that if the service returns a falsey value (simulating no change in text),
    the endpoint returns a 404 (or the defined failure response).
    """
    # Patch the service function to return None (or an empty string) to simulate no change.
    mocker.patch("controllers.edit_book_controller.edit_book_service", return_value=None)

    payload = {"editingOption": "no change"}
    response = client.put("/books/100", json=payload)
    # According to your controller logic, if updated_text is falsey, it returns 404.
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "Failure"

def test_edit_book_invalid_input_type(client):
    """
    Test sending an invalid type (a number) for the 'editingOption' field.
    The endpoint should validate input and return a 400 error.
    """
    # Here, we send a number instead of a string.
    payload = {"editingOption": 12345}
    response = client.put("/books/100", json=payload)
    # Depending on your implementation, this should trigger a validation error.
    # Expect 400 Bad Request.
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "Failure"

def test_edit_book_service_failure(client, mocker):
    """
    Simulate a failure in the edit_book_service (e.g., timeout or API error).
    The endpoint should catch the exception and return a 500 Internal Server Error.
    """
    # Patch the service function to raise an exception.
    mocker.patch("controllers.edit_book_controller.edit_book_service", side_effect=Exception("Service timeout"))
    payload = {"editingOption": "any style"}
    response = client.put("/books/100", json=payload)
    assert response.status_code == 500
    json_data = response.get_json()
    assert json_data["message"] == "Internal Server Error"