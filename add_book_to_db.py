# import csv
from get_book import get_book
# import pandas as pd
import sqlite3
from datetime import datetime


def add_book_to_db(isbns):

    conn = sqlite3.connect('res/books.db')
    cursor = conn.cursor()
    nowdate = datetime.now().date()

    for isbn in isbns:

        cursor.execute('SELECT COUNT(isbn13) FROM popular_books WHERE isbn13 = ?', (isbn,))
        count = cursor.fetchone()[0]
        # 데이터베이스에 없으면
        if count == 0:
            item = get_book(isbn)

            try:
                isbn13 = int(item.get("isbn13"))
                bookname = item.get("bookname")
                authors = item.get("authors")
                publisher = item.get("publisher")
                class_no = item.get("class_no")
                class_nm = item.get("class_nm")
                bookImageURL = item.get("bookImageURL")
                createdAt = nowdate
                cursor.execute('''
                                INSERT INTO popular_books (isbn13, bookname, authors, publisher, class_no, class_nm, bookImageURL, createdAt)
                                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                            ''', (isbn13, bookname, authors, publisher, class_no, class_nm, bookImageURL, createdAt))

                print(f'ISBN {isbn} inserted into database')
            except Exception as e:
                print(f"Failed to get ISBN {str(isbn)} from api")
                return f"Error parsing JSON data: {str(e)}", 400
        # 데이터베이스에 있으면
        else:
            print(f'ISBN {isbn} found in database')

        # # Check if the book already exists in the CSV file
        # file_pd = pd.read_csv("res/book_df.csv")
        # with open("res/book_df.csv", "r") as file:
        #     reader = csv.DictReader(file)
        #     for row in reader:
        #         if int(row["isbn13"]) == int(isbn):
        #             print("Book already exists in the CSV file")
        #             return False
        #
        # # If book does not exist in the CSV file, get the book information and add it to the CSV file
        # book_info = get_book(isbn)
        # print()
        #
        # with open("res/book_df.csv", "a", encoding='utf-8-sig', newline='') as file:
        #
        #     writer = csv.writer(file)
        #     writer.writerow([len(file_pd), book_info["no"]
        #               , ""
        #               , book_info["bookname"]
        #               , book_info["authors"]
        #               , book_info["publisher"]
        #               , book_info["publication_year"]
        #               , book_info["isbn13"]
        #               , ""
        #               , ""
        #               , book_info["class_no"]
        #               , book_info["class_nm"]
        #               , ""
        #               , book_info["bookImageURL"]
        #               , ""])
        #
        #     print("Book added to CSV file")
        #     return True

    # Commit changes and close connection
    conn.commit()
    conn.close()