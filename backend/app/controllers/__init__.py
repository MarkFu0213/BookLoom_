from flask import Blueprint

# Create a blueprint registry
api_bp = Blueprint('api', __name__)
#
# # Import and register controllers
from .user_controller import user_bp
from .mongo_db_controller import mongo_bp
from .edit_book_controller import book_bp
# from .story_controller import story_bp
#
# api_bp.register_blueprint(user_bp, url_prefix='/users')
# api_bp.register_blueprint(book_bp, url_prefix='/books')
# api_bp.register_blueprint(story_bp, url_prefix='/stories')
def book_controller():
    return None