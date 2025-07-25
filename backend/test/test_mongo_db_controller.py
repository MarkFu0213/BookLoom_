import sys
import os
import pytest

# Ensure the "app" folder is in sys.path.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

import json
from flask import Flask
from pymongo.errors import DuplicateKeyError

# Import the blueprint and the collection from your Mongo controller.
from controllers.mongo_db_controller import mongo_bp, books_collection

@pytest.fixture
def app():
    app = Flask(__name__)
    app.register_blueprint(mongo_bp)
    app.config["TESTING"] = True
    return app

@pytest.fixture
def client(app):
    return app.test_client()


def test_create_book_success(client, mocker):
    # Prepare valid book data.
    book_data = {
        "book_serial": 12345,
        "title": "The Great Adventure",
        "author": "John Doe",
        "publication_date": "2024-01-01",
        "tags": "Fantasy, Adventure",
        "rating": "PG-13",
        "total_chapters": 20,
        "total_word_count": 100000,
        "text": "Once upon a time..."
    }
    # Patch the insert_one method to simulate a successful insert.
    fake_result = mocker.Mock()
    fake_result.inserted_id = "fake_id"
    mocker.patch.object(books_collection, "insert_one", return_value=fake_result)

    response = client.post("/books", json=book_data)
    assert response.status_code == 200, response.get_data(as_text=True)
    json_data = response.get_json()
    assert json_data["message"] == "Successful"


def test_create_book_missing_fields(client):
    # Provide incomplete data (e.g., missing required fields).
    incomplete_data = {
        "book_serial": 12345,
        "author": "John Doe"
        # Missing title, publication_date, tags, rating, total_chapters, total_word_count, text.
    }
    response = client.post("/books", json=incomplete_data)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "Failure"
    assert "Missing required fields" in json_data["error"]


def test_get_books(client, mocker):
    # Simulate two sample book documents.
    sample_books = [
        {"_id": "1", "book_serial": 12345, "title": "Book One", "author": "John Doe"},
        {"_id": "2", "book_serial": 67890, "title": "Book Two", "author": "Jane Doe"}
    ]
    mocker.patch.object(books_collection, "find", return_value=sample_books)
    response = client.get("/books")
    assert response.status_code == 200
    json_data = response.get_json()
    assert isinstance(json_data, list)
    assert len(json_data) == 2


def test_get_book_by_serial_success(client, mocker):
    # Simulate a found book document.
    sample_book = {
        "_id": "1",
        "book_serial": 12345,
        "title": "Book One",
        "author": "John Doe",
        "publication_date": "2024-01-01",
        "tags": "Fantasy",
        "rating": "PG-13",
        "total_chapters": 20,
        "total_word_count": 100000,
        "text": "Once upon a time..."
    }
    mocker.patch.object(books_collection, "find_one", return_value=sample_book)
    response = client.get("/books/12345")
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data["book_serial"] == 12345
    assert json_data["title"] == "Book One"


def test_get_book_by_serial_not_found(client, mocker):
    # Simulate no book found by returning None.
    mocker.patch.object(books_collection, "find_one", return_value=None)
    response = client.get("/books/99999")
    assert response.status_code == 404
    json_data = response.get_json()
    assert "error" in json_data
    assert json_data["error"] == "Book not found"

def test_create_duplicate_book(client, mocker):
    """
    Simulate inserting a book with a duplicate book_serial.
    Expect the controller to catch a DuplicateKeyError and return an error message.
    """
    book_data = {
        "book_serial": 55555,
        "title": "Duplicate Book",
        "author": "Jane Doe",
        "publication_date": "2025-01-01",
        "tags": "Drama",
        "rating": "PG",
        "total_chapters": 10,
        "total_word_count": 50000,
        "text": "It was a dark and stormy night..."
    }
    # Simulate the insert raising a DuplicateKeyError.
    mocker.patch.object(books_collection, "insert_one", side_effect=DuplicateKeyError("duplicate key error"))
    response = client.post("/books", json=book_data)
    assert response.status_code == 404
    json_data = response.get_json()
    assert json_data["message"] == "Failure"
    assert "already exists" in json_data["error"].lower()

def test_create_book_invalid_types(client):
    # All required fields present, but book_serial is a string instead of int
    book_data = {
        "book_serial": "12345",          # wrong type
        "title": "Type Test",
        "author": "Tester",
        "publication_date": "2024-01-01",
        "tags": "Test",
        "rating": "PG",
        "total_chapters": 5,
        "total_word_count": 2500,
        "text": "Some content"
    }
    response = client.post("/books", json=book_data)
    assert response.status_code == 404
    data = response.get_json()
    assert data["message"] == "Failure"
    assert data["error"] == "Invalid data types"


def test_create_book_unexpected_error(client, mocker):
    # Valid payload, but insert_one raises a generic Exception
    book_data = {
        "book_serial": 54321,
        "title": "Error Test",
        "author": "Tester",
        "publication_date": "2024-01-01",
        "tags": "Test",
        "rating": "PG",
        "total_chapters": 5,
        "total_word_count": 2500,
        "text": "Some content"
    }
    mocker.patch.object(
        books_collection,
        "insert_one",
        side_effect=Exception("boom")
    )

    response = client.post("/books", json=book_data)
    assert response.status_code == 500
    data = response.get_json()
    assert data["message"] == "Failure"
    assert "boom" in data["error"]
