from config.mongodb_db import mongo_db

def get_book_by_serial(book_serial):
    try:
        book = mongo_db.books.find_one({"book_serial": book_serial})
        return book if book else None
    except Exception as e:
        print(f"Database Error: {str(e)}")
        return None

def update_book_text(book_serial, updated_text):
    try:
        result = mongo_db.books.update_one(
            {"book_serial": book_serial},
            {"$set": {"text": updated_text}}
        )
        return result.modified_count > 0
    except Exception as e:
        print(f"Database Error: {str(e)}")
        return False
