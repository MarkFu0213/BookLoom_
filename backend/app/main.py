from flask import Flask

from flask_cors import CORS


# from backend.app.controllers import mongo_bp

from controllers import mongo_bp
# from database import db_session  # Database connection
from controllers.user_controller import user_bp
# from controllers.book_controller import book_bp
# from app.controllers.story_controller import story_bp
from controllers.edit_book_controller import book_bp

def create_app():
    app = Flask(__name__)

    # Register Blueprints (controllers)
    app.register_blueprint(user_bp)
    app.register_blueprint(mongo_bp)
    app.register_blueprint(book_bp)
    # app.register_blueprint(story_bp, url_prefix='/api/stories')

    # Configure the app (add any configurations here)
    # app.config["JSONIFY_PRETTYPRINT_REGULAR"] = True

    return app

# Initialize the application
app = create_app()
CORS(app)
# Run the server
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)

# # Cleanup database session after each request
# @app.teardown_appcontext
# def shutdown_session(exception=None):
#     db_session.remove()
