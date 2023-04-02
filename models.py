from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# db 경로 설정
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////res/book.db'
db = SQLAlchemy(app)

class PopularBooks(db.Model):
    __tablename__ = 'popular_books'

    isbn13 = db.Column(db.Integer, primary_key=True)
    bookname = db.Column(db.String(128))
    authors = db.Column(db.String(128))
    publisher = db.Column(db.String(128))
    class_no = db.Column(db.String(32))
    class_nm = db.Column(db.String(128))
    bookImageURL = db.Column(db.String(128))