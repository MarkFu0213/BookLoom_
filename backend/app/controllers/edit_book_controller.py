from flask import Blueprint, request, jsonify
from services.edit_book_service import edit_book_service

book_bp = Blueprint('book_bp', __name__)


@book_bp.route('/books/<int:book_serial>', methods=['PUT'])
def edit_book(book_serial):
    data = request.get_json()
    editing_option = data.get('editingOption')

    if not editing_option:
        return jsonify({"message": "Missing editing option"}), 400

    try:
        # Call the service layer to process the book edit request
        updated_text = edit_book_service(book_serial, editing_option)
        if updated_text:
            return jsonify({
                "message": "Chapter updated successfully",
                "text": updated_text
            }), 201
        else:
            return jsonify({"message": "Failure"}), 404
    except Exception as e:
        print(f"Error in edit_book: {str(e)}")
        return jsonify({"message": "Internal Server Error"}), 500
