from flask import Blueprint, request, jsonify
from config.mysql_db import SessionLocal  # SQLAlchemy database connection
from services.user_service import UserService

user_bp = Blueprint('user_bp', __name__)

# =========================
# Authentication Endpoints
# =========================

@user_bp.route('/auth/register', methods=['POST'])
def register():
    """
    POST /auth/register
    Request Body:
    {
        "username": "string",
        "email": "string",
        "password": "string",
        "age": number,
        "gender": "string",
        "favoriteBook": "string",
        "favoriteAuthor": "string",
        "preferredGenre": "string"
    }
    Response:
    {
        "message": "User registered successfully",
        "userId": "string"
    }
    """
    data = request.get_json()
    required_fields = [
        'username', 'email', 'password', 'age',
        'gender', 'favoriteBook', 'favoriteAuthor', 'preferredGenre'
    ]
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing field: {field}'}), 400

    db = SessionLocal()
    try:
        # Call the service layer to create a user
        user = UserService.create_user(
            db,
            username=data['username'],
            email=data['email'],
            password=data['password'],
            age=data['age'],
            gender=data['gender'],
            fav_book=data['favoriteBook'],
            fav_author=data['favoriteAuthor'],
            preferred_genre=data['preferredGenre']
        )

        response = {
            "message": "User registered successfully",
            "userId": str(user.user_id)
        }
        return jsonify(response), 201
    except ValueError as ve:
        db.rollback()
        return jsonify({'error': str(ve)}), 400  # Business validation error
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500  # Internal server error
    finally:
        db.close()


@user_bp.route('/auth/login', methods=['POST'])
def login():
    """
    POST /auth/login
    Request Body:
    {
        "username": "string",
        "password": "string"
    }
    Response:
    {
        "userId": "string",
        "email": "string",
        "age": number,
        "gender": "string",
        "favoriteBook": "string",
        "favoriteAuthor": "string",
        "preferredGenre": "string"
    }
    """
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password are required'}), 400

    db = SessionLocal()
    try:
        # Authenticate user using service layer
        user = UserService.authenticate_user(db, data['username'], data['password'])
        if user:
            response = {
                "userId": str(user.user_id),
                "email": user.email,
                "age": user.age,
                "gender": user.gender,
                "favoriteBook": user.fav_book,
                "favoriteAuthor": user.fav_author,
                "preferredGenre": user.preferred_genre
            }
            return jsonify(response), 200
        else:
            return jsonify({'error': 'Invalid username or password'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


# =========================
# User Profile Management
# =========================

@user_bp.route('/users/<int:user_id>/profile', methods=['GET'])
def get_user_profile(user_id):
    """
    Retrieves a user's profile details.
    """
    db = SessionLocal()
    try:
        user = UserService.get_user_by_id(db, user_id)
        if user:
            return jsonify({
                "username": user.username,
                "email": user.email,
                "age": user.age,
                "gender": user.gender,
                "favoriteBook": user.fav_book,
                "favoriteAuthor": user.fav_author,
                "preferredGenre": user.preferred_genre
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()


@user_bp.route('/users/<int:user_id>/profile', methods=['PUT'])
def update_profile(user_id):
    """
    Updates user profile information.
    """
    data = request.get_json()
    allowed_fields = ['username', 'email', 'age', 'gender', 'favoriteBook', 'favoriteAuthor', 'preferredGenre']

    if not any(field in data for field in allowed_fields):
        return jsonify({'error': 'No valid fields provided for update'}), 400

    db = SessionLocal()
    try:
        updated_user = UserService.update_user_profile(db, user_id, data)
        if updated_user:
            return jsonify({
                "message": "Profile updated successfully",
                "updatedProfile": {
                    "username": updated_user.username,
                    "email": updated_user.email,
                    "age": updated_user.age,
                    "gender": updated_user.gender,
                    "favoriteBook": updated_user.fav_book,
                    "favoriteAuthor": updated_user.fav_author,
                    "preferredGenre": updated_user.preferred_genre
                }
            }), 200
        else:
            return jsonify({'error': 'User not found'}), 404
    except Exception as e:
        db.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()

@user_bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    DELETE /users/{userId}
    Description: Permanently deletes a user's account.
    Response:
    {
        "message": "User deleted successfully"
    }
    """
    db = SessionLocal()
    try:
        result = UserService.delete_user(db, user_id)
        if result:
            return jsonify({"message": "User deleted successfully"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        db.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.close()

@user_bp.route('/auth/logout', methods=['POST'])
def logout():
    """
    Logs out a user (optional, can just be handled client-side).
    Request Body:
    {
        "username": "string"
    }
    Response:
    {
        "message": "User logged out"
    }
    """
    data = request.get_json()
    if not data or 'username' not in data:
        return jsonify({'error': 'Username is required'}), 400

    db = SessionLocal()
    try:
        logout_success = UserService.logout_user(db, data['username'])
        if logout_success:
            return jsonify({"message": "User logged out"}), 200
        else:
            return jsonify({"error": "User not found"}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        db.close()