# backend/app/mappers/book_mapper.py
from pymongo.errors import DuplicateKeyError
from app.config.mongodb_db import mongo_db

class BookMapper:
  def __init__(self):
    self.collection = mongo_db["books"]

  def create_book(self, book_data):
    """创建新书"""
    try:
      result = self.collection.insert_one(book_data)
      return str(result.inserted_id), None
    except DuplicateKeyError:
      return None, "Book with this book_serial already exists"
    except Exception as e:
      return None, str(e)

  def get_all_books(self):
    """获取所有书的元数据（不包括text）"""
    books = list(self.collection.find({}, {"text": 0}))
    for book in books:
      book["_id"] = str(book["_id"])
    return books

  def get_book_by_serial(self, book_serial):
    """通过book_serial获取完整书信息"""
    book = self.collection.find_one({"book_serial": book_serial})
    if book:
      book["_id"] = str(book["_id"])
    return book

  def get_book_text(self, book_serial):
    """获取书的text内容"""
    book = self.collection.find_one({"book_serial": book_serial}, {"text": 1})
    return book["text"] if book else None

  def update_book_text(self, book_serial, text):
    """更新书的text内容"""
    result = self.collection.update_one(
        {"book_serial": book_serial},
        {"$set": {"text": text}}
      )
    return result.matched_count > 0

  def delete_book(self, book_serial):
    """删除书"""
    result = self.collection.delete_one({"book_serial": book_serial})
    return result.deleted_count > 0