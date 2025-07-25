import sys
import os
from types import SimpleNamespace
import pytest

# Ensure the "app" folder is in sys.path.
# (Assuming this file is in backend/test and your service code is in backend/app)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../app")))

from openai import OpenAI, OpenAIError
from config import OPENAI_API_KEY
from mappers.edit_book_mapper import get_book_by_serial, update_book_text
from services.edit_book_service import edit_book_service


# ----------------------------
# Test: Book Not Found
# ----------------------------
def test_edit_book_book_not_found(mocker):
    # Patch get_book_by_serial to return None (book not found)
    mocker.patch("mappers.edit_book_mapper.get_book_by_serial", return_value=None)

    result = edit_book_service(123, "some style")
    assert result is None, "If book is not found, the service should return None."


# ----------------------------
# Test: Successful Edit
# ----------------------------
def test_edit_book_success(mocker):
    original_book = {"book_serial": 123, "text": "This is the original text."}
    # Patch both get_book_by_serial and update_book_text as they appear in services.edit_book_service.
    mocker.patch("services.edit_book_service.get_book_by_serial", return_value=original_book)

    fake_completion = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="This is the updated text."))]
    )
    fake_client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kwargs: fake_completion))
    )
    mocker.patch("services.edit_book_service.OpenAI", return_value=fake_client)

    mocker.patch("services.edit_book_service.update_book_text", return_value=True)

    result = edit_book_service(123, "change style")
    assert result == "This is the updated text.", "The service should return the updated text from OpenAI."
    assert result != original_book["text"], "The updated text should differ from the original."


# ----------------------------
# Test: Update Failure in Database
# ----------------------------
def test_edit_book_update_failure(mocker):
    # Set up a fake original book.
    original_book = {"book_serial": 123, "text": "Original text."}
    mocker.patch("mappers.edit_book_mapper.get_book_by_serial", return_value=original_book)

    # Create a fake OpenAI response with updated text.
    fake_completion = SimpleNamespace(
        choices=[SimpleNamespace(message=SimpleNamespace(content="New updated text."))]
    )
    fake_client = SimpleNamespace(
        chat=SimpleNamespace(completions=SimpleNamespace(create=lambda **kwargs: fake_completion)))
    mocker.patch("services.edit_book_service.OpenAI", return_value=fake_client)

    # Patch update_book_text to return False (simulating a failure to update in the database).
    mocker.patch("mappers.edit_book_mapper.update_book_text", return_value=False)

    result = edit_book_service(123, "change style")
    assert result is None, "If the database update fails, the service should return None."


# ----------------------------
# Test: OpenAI Error Handling
# ----------------------------
def test_edit_book_openai_error(mocker):
    # 1) Ensure the service sees a book, so we skip the "not found" early return.
    original_book = {"book_serial": 123, "text": "Original text."}
    mocker.patch(
        "services.edit_book_service.get_book_by_serial",
        return_value=original_book
    )

    # 2) Make OpenAI.chat.completions.create raise an OpenAIError.
    def fake_create(**kwargs):
        raise OpenAIError("Simulated OpenAI error")
    fake_client = SimpleNamespace(
        chat=SimpleNamespace(
            completions=SimpleNamespace(create=fake_create)
        )
    )
    mocker.patch("services.edit_book_service.OpenAI", return_value=fake_client)

    # 3) Call the service; it should catch the OpenAIError and return None.
    result = edit_book_service(123, "change style")
    assert result is None, "If the OpenAI call fails, the service should return None."

