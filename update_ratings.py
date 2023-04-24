import requests
import sqlite3
import json
import xmltodict
from datetime import datetime

def update_ratings(isForced):
    # XML 데이터 가져오기
    libraryUrl = "http://data4library.kr/api/loanItemSrch?authKey=32bb82a55e2ccb6dd8baec16309bed7ecc2985e9a07e83dc18b5037179636d55&startDt=2023-01-01&endDt=2023-04-01"
    # headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}

    postData = {'url': libraryUrl}
    response = requests.post('http://43.200.106.28:4000/library', json=postData)

    xml_data = xmltodict.parse(response.text)

    jsonData = json.dumps(xml_data, ensure_ascii=False)

    jsonObject = json.loads(jsonData)

    docs = jsonObject.get("response").get("docs")

    # SQLite database 연결
    conn = sqlite3.connect('res/books.db')
    cursor = conn.cursor()

    # 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS popular_books (
            isbn13 INTEGER PRIMARY KEY,
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
    if isForced or str(cursor.execute('SELECT createdAt from popular_books LIMIT 1').fetchone()[0]) != str(nowdate):

        # 테이블에서 모두 삭제
        cursor.execute('DELETE from popular_books')

        # 테이블에 삽입
        for item in docs.get("doc"):
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

        print("Data saved successfully!")

    else:
        print("No data has been updated. : Same date")

    cursor.execute("SELECT COUNT(*) FROM popular_books")
    popular_books_total_num = cursor.fetchone()[0]

    # Commit changes and close connection
    conn.commit()
    conn.close()

    return popular_books_total_num