import pymysql

try:
    # Replace with your MySQL credentials
    connection = pymysql.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="your_database"
    )

    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES;")
        tables = cursor.fetchall()
        print("✅ MySQL connection successful! Tables:", tables)

    connection.close()
except Exception as e:
    print("❌ MySQL connection failed:", e)
