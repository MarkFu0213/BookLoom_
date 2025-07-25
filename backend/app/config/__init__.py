from .mysql_db import engine, SessionLocal  # Expose engine for other modules
from .mongodb_db import mongo_db
from .settings import OPENAI_API_KEY, DATABASE_URL, MONGO_URI