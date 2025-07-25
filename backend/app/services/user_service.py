from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import Session
from models.user_model import User
from mappers.user_mapper import UserMapper

class UserService:
    @staticmethod
    def create_user(db: Session, username, email, password, age, gender, fav_book, fav_author, preferred_genre):
        """
        Creates a new user in the database.

        :param db: SQLAlchemy session
        :param username: str
        :param email: str
        :param password: str
        :param age: int
        :param gender: str
        :param fav_book: str
        :param fav_author: str
        :param preferred_genre: str
        :return: Created User object
        """
        # Hash the password
        # hashed_password = generate_password_hash(password)
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")
        # hashed_password = password
        # Create User object
        new_user = User(
            username=username,
            email=email,
            password_hash=hashed_password,
            age=age,
            gender=gender,
            fav_book=fav_book,
            fav_author=fav_author,
            preferred_genre=preferred_genre
        )

        return UserMapper.create_user(db, new_user)

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str):
        """
        Authenticates a user by checking their credentials.

        :param db: SQLAlchemy session
        :param username: str
        :param password: str
        :return: User object if authentication is successful, else None
        """
        user = UserMapper.get_user_by_username_or_email(db, username, username)
        if user and check_password_hash(user.password_hash, password):
            return user
        return None

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return UserMapper.get_user_by_id(db, user_id)

    @staticmethod
    def update_user_profile(db: Session, user_id: int, data: dict):
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None

        # Map camelCase API fields to snake_case DB fields 
        if 'username' in data:
            user.username = data['username']
        if 'email' in data:
            user.email = data['email']
        if 'age' in data:
            user.age = data['age']
        if 'gender' in data:
            user.gender = data['gender']
        if 'favoriteBook' in data:
            user.fav_book = data['favoriteBook']  # Map from camelCase to snake_case
        if 'favoriteAuthor' in data:
            user.fav_author = data['favoriteAuthor']  # Map from camelCase to snake_case
        if 'preferredGenre' in data:
            user.preferred_genre = data['preferredGenre']  # Map from camelCase to snake_case
        
        # Add debug logging
        print(f"Updating user {user_id} with data: {data}")
        
        # Make sure we commit the changes to the database
        db.commit()
        
        # Verify the update worked
        print(f"User updated successfully: {user.username}, fav_book: {user.fav_book}")
        
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        return UserMapper.delete_user(db, user_id)

    @staticmethod
    def logout_user(db: Session, username: str):
        """
        Handles user logout. (Optional: Can be expanded for session handling)
        """
        user = UserMapper.get_user_by_username(db, username)
        if user:
            # If using sessions, you could clear tokens or mark user as logged out in the DB.
            return True  # Indicating successful logout
        return False  # User not found
