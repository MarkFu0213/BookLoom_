DROP DATABASE IF EXISTS BookLoomMySQL;

CREATE DATABASE BookLoomMySQL;

USE BookLoomMySQL;

-- Users Table (Authentication & Preferences)
CREATE TABLE users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    age INT CHECK (age >= 0),  -- Ensure age is non-negative
    gender ENUM('Male', 'Female', 'Other', 'Prefer not to say') NOT NULL,
    fav_book VARCHAR(255),  -- Favorite book
    fav_author VARCHAR(255),  -- Favorite author
    preferred_genre ENUM('fiction', 'nonfiction') NOT NULL,  -- Preferred reading type
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP  -- Auto-set timestamp for account creation
);

-- Books Table (Book Metadata & Serial Reference)
CREATE TABLE books (
    book_serial INT PRIMARY KEY AUTO_INCREMENT,  -- Unique serial number
    title VARCHAR(255) NOT NULL,
    author VARCHAR(255),
    publication_date DATE,
    tags VARCHAR(255),  -- Comma-separated genres
    rating VARCHAR(10), -- Age rating (PG, PG-13, etc.)
    total_chapters INT,
    total_word_count INT
);