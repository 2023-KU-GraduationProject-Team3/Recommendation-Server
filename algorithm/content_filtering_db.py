#!/usr/bin/env python
# coding: utf-8

# In[9]:
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
import json
import sqlite3
import numpy as np
from get_book import get_book

import warnings


warnings.filterwarnings("ignore")

def content_algorithm_db(favorites, result_num):
    conn = sqlite3.connect('res/books.db')

    books_df = pd.read_sql_query('SELECT isbn13, bookname, authors, publisher, class_no, class_nm, bookImageURL, createdAt FROM popular_books', conn)

    for isbn in favorites:
        book_data = get_book(isbn)
        try:
            new_df = [int(book_data.get('isbn13')), book_data.get('bookname'),book_data.get('authors'), book_data.get('publisher'), book_data.get('class_no'), book_data.get('class_nm'), book_data.get('bookImageURL'), '0']
            books_df.loc[len(books_df)] = new_df
            #print('Book added successfully')
        except Exception as e:
            print('Failed to add books to book_df')
            print(str(e))
            return e;

    books_df['same_author'] = books_df.apply(lambda x: x['authors'] if x['authors'] == x['authors'] else '', axis=1)
    books_df['same_publisher'] = books_df.apply(lambda x: x['publisher'] if x['publisher'] == x['publisher'] else '', axis=1)

    # 가중치 값
    bookname_weight = 0.0
    author_weight = 0.5
    publisher_weight = 0.0
    class_nm_weight = 0.5

    # Tf-Idf vectorizer 생성하고 각 요소마다 행렬을 만듦
    tfidf_bookname = TfidfVectorizer(stop_words='english')
    tfidf_bookname_matrix = tfidf_bookname.fit_transform(books_df['bookname'])

    tfidf_author = TfidfVectorizer(stop_words='english')
    tfidf_author_matrix = tfidf_author.fit_transform([str(val) for val in books_df['same_author'] if val is not np.nan])

    tfidf_publisher = TfidfVectorizer(stop_words='english')
    tfidf_publisher_matrix = tfidf_publisher.fit_transform([str(val) for val in books_df['same_publisher'] if val is not np.nan])

    tfidf_class_nm = TfidfVectorizer(stop_words='english')
    tfidf_class_nm_matrix = tfidf_class_nm.fit_transform(books_df['class_nm'].values.astype('U'))

    # hstack을 이용해서 행렬을 쌓고 가중치 곱하기
    weighted_matrix = hstack([tfidf_bookname_matrix * bookname_weight, tfidf_author_matrix * author_weight,
                              tfidf_publisher_matrix * publisher_weight, tfidf_class_nm_matrix * class_nm_weight])


    # isbn_array로 받은 ISBN들과 일치하는 책들을 isbn_books에 넣기
    isbn_books = []

    for isbn in favorites:
        isbn_books.append(books_df[books_df['isbn13'] == isbn].index[0])

    similarities = cosine_similarity(weighted_matrix[isbn_books], weighted_matrix)

    similar_indices = similarities.argsort()[0][::-1][1:result_num + 1]

    recommended_books = []
    for i in similar_indices:
        recommended_books.append({
            'isbn13': int(books_df.iloc[i]['isbn13']),
            'bookname': str(books_df.iloc[i]['bookname']),
            'authors': str(books_df.iloc[i]['authors']),
            'publisher': str(books_df.iloc[i]['publisher']),
            'class_no': str(books_df.iloc[i]['class_no']),
            'class_nm': str(books_df.iloc[i]['class_nm']),
            'bookImageURL': str(books_df.iloc[i]['bookImageURL'])
        })

    conn.close()
    return json.dumps(recommended_books, ensure_ascii=False)
