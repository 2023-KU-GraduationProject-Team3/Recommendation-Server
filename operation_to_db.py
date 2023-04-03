from get_book import get_book
import sqlite3
from datetime import datetime

def add_book_to_db(isbns):
    conn = sqlite3.connect('res/books.db')
    cursor = conn.cursor()
    nowdate = datetime.now().date()

    # 추가된 도서 개수
    added_books_num = 0

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
                added_books_num += added_books_num
            except Exception as e:
                print(f"Failed to get ISBN {str(isbn)} from api")
                return f"Error parsing JSON data: {str(e)}", 400
        # 데이터베이스에 있으면
        else:
            print(f'ISBN {isbn} found in database')

    # Commit changes and close connection
    conn.commit()
    conn.close()
    return added_books_num



def delete_book_from_db(fixed_rows):

    conn = sqlite3.connect('res/books.db')
    cursor = conn.cursor()

    try:
        cursor.execute(f"SELECT COUNT(*) FROM popular_books")
        total_rows = cursor.fetchone()[0]
        if fixed_rows >= total_rows:
            # No rows to delete, return an appropriate response
            response = f"No rows to delete. Total rows: {total_rows}"
            print(response)
        else:
            cursor.execute(f"SELECT rowid FROM popular_books LIMIT {fixed_rows}")
            top_rows = [row[0] for row in cursor.fetchall()]
            cursor.execute(f"DELETE FROM popular_books WHERE rowid NOT IN ({','.join(map(str, top_rows))})")
            conn.commit()
            response = f"{len(top_rows)} rows kept. {total_rows - len(top_rows)} rows deleted."
            print(response)

    except Exception as e:
        print(f'Failed: error {e}')

    # Commit changes and close connection
    conn.commit()
    conn.close()