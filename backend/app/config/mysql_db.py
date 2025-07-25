from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
import os




# MySQL Connection settings
MYSQL_USER = "root"

# If you want to retrieve password from env, do the following command with the your_password replaced in your terminal:
# On macOS/Linux:
# export MYSQL_PASSWORD="your_password"
# On Windows (Command Prompt):
# set MYSQL_PASSWORD=your_password

# MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")  # Retrieve from environment variable
# print(MYSQL_PASSWORD)
# If you want to hard code in file, uncomment the line below
MYSQL_PASSWORD = "Miracle%40123%40"  # Replace with your password
MYSQL_HOST = "localhost"
MYSQL_PORT = "3306"
MYSQL_DATABASE = "BookLoomMySQL"

DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
engine = create_engine(DATABASE_URI)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def execute_sql_script():
    with open("../../database/BookLoomMySQL.sql", "r") as file:
        sql_script = file.read()
    with engine.connect() as connection:
        for statement in sql_script.split(";"):
            if statement.strip():
                connection.execute(text(statement))
        connection.commit()
    print("✅ MySQL database initialized successfully!")

# Run this function during initial setup
# execute_sql_script()
