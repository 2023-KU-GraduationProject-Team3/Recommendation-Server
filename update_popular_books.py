import requests
import sqlite3
import json
import xmltodict
import uuid
from datetime import datetime, date, timedelta

def update_popular_books(isForced):

    # 오늘 날짜
    today = date.today()

    # 어제 날짜
    yesterday = today - timedelta(days=1)
    # 어제 날짜 변수
    yesterday_date = yesterday.strftime("%Y-%m-%d")

    # 2년 전 날짜
    two_years_ago = yesterday - timedelta(days=365 * 2)
    # 2년 전 날짜 변수
    two_years_ago_date = two_years_ago.strftime("%Y-%m-%d")

    # 추천에 활용할 책 개수
    book_num = 5000

    # SQLite database 연결
    conn = sqlite3.connect('res/books.db')
    cursor = conn.cursor()

    # 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS popular_books (
            id TEXT PRIMARY KEY,
            isbn13 INTEGER,
            bookname TEXT,
            authors TEXT,
            publisher TEXT,
            class_no TEXT,
            class_nm TEXT,
            bookImageURL TEXT,
            createdAt TEXT
        )
    ''')

    nowdate = datetime.now().date()

    # 이전에 업데이트 했던 날짜와 같지 않을 때만 실행
    if isForced or int(cursor.execute('SELECT COUNT(*) FROM popular_books').fetchone()[0]) == 0 or str(cursor.execute('SELECT createdAt from popular_books LIMIT 1').fetchone()[0]) != str(nowdate):

        # XML 데이터 가져오기
        libraryUrl = f"http://data4library.kr/api/loanItemSrch?authKey=32bb82a55e2ccb6dd8baec16309bed7ecc2985e9a07e83dc18b5037179636d55&startDt={two_years_ago_date}&endDt={yesterday_date}&pageSize={book_num}"

        print(libraryUrl)
        postData = {'url': libraryUrl}
        response = requests.post('http://43.200.106.28:4000/library', json=postData)
        xml_data = xmltodict.parse(response.text)
        jsonData = json.dumps(xml_data, ensure_ascii=False)
        jsonObject = json.loads(jsonData)
        docs = jsonObject.get("response").get("docs")

        # 테이블에서 모두 삭제
        cursor.execute('DELETE from popular_books')

        # 테이블에 삽입
        for item in docs.get("doc"):
            id = str(uuid.uuid4())
            isbn13 = int(item.get("isbn13"))
            bookname = item.get("bookname")
            authors = item.get("authors")
            publisher = item.get("publisher")
            class_no = item.get("class_no")
            class_nm = item.get("class_nm")
            bookImageURL = item.get("bookImageURL")
            createdAt = nowdate
            cursor.execute('''
                INSERT INTO popular_books (id, isbn13, bookname, authors, publisher, class_no, class_nm, bookImageURL, createdAt)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (id, isbn13, bookname, authors, publisher, class_no, class_nm, bookImageURL, createdAt))

        print("Data saved successfully!")

    else:
        print("No data has been updated. : Same date")

    cursor.execute("SELECT COUNT(*) FROM popular_books")
    popular_books_total_num = cursor.fetchone()[0]

    # Commit changes and close connection
    conn.commit()
    conn.close()

    return popular_books_total_num