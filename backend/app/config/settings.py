import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# General App Settings
SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")
FLASK_ENV = os.getenv("FLASK_ENV", "development")
DEBUG = os.getenv("DEBUG", "True") == "True"

# Database Settings
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://user:password@localhost/bookloom")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/bookloom")

# # Authentication
# JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret")

# OpenAI API Key (if applicable)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# print(OPENAI_API_KEY)
# Rate Limiting (if needed)
API_RATE_LIMIT = os.getenv("API_RATE_LIMIT", "100 per hour")
