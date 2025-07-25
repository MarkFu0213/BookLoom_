# backend/app/controllers/mongo_db_controller.py
from flask import Blueprint, request, jsonify
from pymongo.errors import DuplicateKeyError

from config.mongodb_db import mongo_db
# from config.mongodb_db import mongo_db

# Collections
books_collection = mongo_db["books"]
authors_collection = mongo_db["authors"]

# Blueprint for MongoDB routes
mongo_bp = Blueprint('mongo', __name__)

@mongo_bp.route('/books', methods=['POST'])
def create_book():
  """
  Create a new book
  Request Body:
  {
    "book_serial": 12256,
    "title": "The Great Adventure",
    "author": "John Doe",
    "publication_date": "2024-01-01",
    "tags": "Fantasy, Adventure",
    "rating": "PG-13",
    "total_chapters": 20,
    "total_word_count": 100000,
    "text": "Once.."
  }
  Response: { "message": "Book created"}
  """
  data = request.get_json()
  required_fields = ["book_serial", "title", "author", "publication_date",
                     "tags", "rating", "total_chapters", "total_word_count", "text"]

  if not all(field in data for field in required_fields):
    return jsonify({"message": "Failure", "error": "Missing required fields"}), 404

  # Validate data types
  if not (isinstance(data["book_serial"], int) and
          isinstance(data["title"], str) and
          isinstance(data["author"], str) and
          isinstance(data["publication_date"], str) and
          isinstance(data["tags"], str) and
          isinstance(data["rating"], str) and
          isinstance(data["total_chapters"], int) and
          isinstance(data["total_word_count"], int) and
          isinstance(data["text"], str)):
    return jsonify({"message": "Failure", "error": "Invalid data types"}), 404

  try:
    result = books_collection.insert_one(data)
    return jsonify({"message": "Successful"}), 200
  except DuplicateKeyError:
    return jsonify({"message": "Failure", "error": "Book with this book_serial already exists"}), 404
  except Exception as e:
    return jsonify({"message": "Failure", "error": str(e)}), 500


@mongo_bp.route('/books', methods=['GET'])
def get_books():
  """
  Get all books
  Response:
  {
    "book_serial": 12256,
    "title": "The Great Adventure",
    "author": "John Doe",
    "publication_date": "2024-01-01",
    "tags": "Fantasy, Adventure",
    "rating": "PG-13",
    "total_chapters": 20,
    "total_word_count": 100000
  }
  """
  books = list(books_collection.find({}, {"text": 0}))  # Exclude text field from listing
  for book in books:
    book["_id"] = str(book["_id"])
  return jsonify(books), 200

@mongo_bp.route('/books/<int:book_serial>', methods=['GET'])
def get_book_by_serial(book_serial):
  """
  Get a book by book_serial
  Response:
  {
    "book_serial": 12256,
    "title": "The Great Adventure",
    "author": "John Doe",
    "publication_date": "2024-01-01",
    "tags": "Fantasy, Adventure",
    "rating": "PG-13",
    "total_chapters": 20,
    "total_word_count": 100000,
    "text": "Once upon a time ..",
  }
  """
  book = books_collection.find_one({"book_serial": book_serial})
  if not book:
    return jsonify({"error": "Book not found"}), 404
  book["_id"] = str(book["_id"])
  return jsonify(book), 200