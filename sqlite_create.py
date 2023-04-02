import sqlite3

conn = sqlite3.connect('res/book.db')
conn.execute('CREATE TABLE POPULAR_BOOKS (NAME TEXT, ADDR TEXT, CITY TEXT, PIN TEXT)')
print('Table created successfully')
conn.close()