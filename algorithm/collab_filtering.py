#!/usr/bin/env python
# coding: utf-8

# In[9]:
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
from surprise import Reader, Dataset, SVD
import json

from scipy.sparse.linalg import svds
import warnings


warnings.filterwarnings("ignore")

def collab_algorithm(user_id, result_num=10):
    # rating csv 파일 일기
    ratings_df = pd.read_csv('res/ratings_final_ISBN3.csv')

    # 도서 csv 파일 일기
    books_df = pd.read_csv('res/book_df.csv')

    # reader object 생성
    reader = Reader(rating_scale=(1, 5))

    # surprise Dataset에 reader 넣기
    data = Dataset.load_from_df(ratings_df[['userId', 'isbn13', 'rating']], reader)

    # SVD model
    svd = SVD()
    trainset = data.build_full_trainset()
    svd.fit(trainset)

    # 모든 책을 isbn으로 가져오기
    all_books = list(set(ratings_df['isbn13'].unique()).intersection(set(books_df['isbn13'].unique())))

    # 입력 받은 user에 대해 도서 isbn과 평점 리스트 생성
    user_estimates = []
    for book_id in all_books:
        user_estimates.append((book_id, svd.predict(user_id, book_id).est))

    # 평점 내림차순으로 리스트 정렬하기
    sorted_estimates = sorted(user_estimates, key=lambda x: x[1], reverse=True)


    # 위에서부터 n개 도서 가져오기
    recommended_books = []
    # for i in range(result_num):
    #     isbn = sorted_estimates[i][0]
    #     bookname = books_df.loc[books_df['isbn13'] == isbn, 'bookname'].iloc[0]
    #     recommended_books.append({"isbn13": int(isbn), "bookname": str(bookname)})

    if result_num > len(sorted_estimates):
        result_num = len(sorted_estimates)

    for i in range(result_num):
        isbn = sorted_estimates[i][0]
        # book_info = books_df.loc[books_df['isbn13'] == isbn].iloc[0].to_dict()
        book_info = books_df.loc[books_df['isbn13'] == isbn, ['isbn13', 'bookname', 'authors', 'publisher', 'publication_year', 'class_no', 'class_nm', 'bookImageURL']].iloc[0].to_dict()
        recommended_books.append(book_info)

    return json.dumps(recommended_books, ensure_ascii=False)
