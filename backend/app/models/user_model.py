from sqlalchemy import Column, Integer, String, Enum, CheckConstraint, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base
from config.mysql_db import engine  # Import MySQL connection

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(255), unique=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    age = Column(Integer, CheckConstraint('age >= 0'))
    gender = Column(Enum('Male', 'Female', 'Other', 'Prefer not to say'), nullable=False)
    fav_book = Column(String(255))
    fav_author = Column(String(255))
    preferred_genre = Column(Enum('fiction', 'nonfiction'), nullable=False)
    created_at = Column(TIMESTAMP, server_default=text('CURRENT_TIMESTAMP'))

# Create tables in MySQL if they don't exist
Base.metadata.create_all(bind=engine)