from sqlalchemy.orm import Session
from models.user_model import User
from sqlalchemy import or_

class UserMapper:
    @staticmethod
    def get_user_by_username_or_email(db: Session, username: str, email: str):
        return db.query(User).filter(or_(User.username == username, User.email == email)).first()

    @staticmethod
    def create_user(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        return db.query(User).filter(User.user_id == user_id).first()

    @staticmethod
    def update_user_profile(db: Session, user_id: int, update_data: dict):
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            return None

        for key, value in update_data.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user


    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            db.delete(user)
            db.commit()
            return True
        return False

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()