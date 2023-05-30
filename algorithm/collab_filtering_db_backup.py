#!/usr/bin/env python
# coding: utf-8

# In[9]:
import pandas as pd
from surprise import Reader, Dataset, SVD
import json
import sqlite3
from surprise.model_selection import train_test_split

import warnings

from get_review_data import get_review_data
from get_book import get_book


warnings.filterwarnings("ignore")

def collab_algorithm_db_backup(user_id, result_num=10):
    conn = sqlite3.connect('res/books.db')

    # rating csv 파일 읽기
    # ratings_df = pd.read_csv('res/ratings_final_ISBN3.csv')

    review_json = get_review_data()

    ratings_df = pd.DataFrame.from_dict(review_json)

    print(ratings_df)

    # Surprise dataset으로 변환
    reader = Reader(rating_scale=(1, 10))
    dataset = Dataset.load_from_df(ratings_df[['user_id', 'book_isbn', 'review_rating']], reader)

    # training으로 dataset을 나누고 테스트하기
    trainset, testset = train_test_split(dataset, test_size=0.2)

    # training set에서 SVD model train
    model = SVD()
    model.fit(trainset)

    # 유저의 도서 isbn과 별점 가져오기
    user_ratings = ratings_df.loc[ratings_df['user_id'] == user_id, ['book_isbn', 'review_rating']]

    # 모든 책에 대해 별점 예측하기
    all_books = ratings_df['book_isbn'].unique()
    predictions = []
    for book in all_books:
        prediction = model.predict(user_id, book)
        #predictions.append(book)
        # 점수도 함께 저장
        predictions.append((book, prediction.est))

    # Sort the predictions by predicted rating
    predictions.sort(key=lambda x: x[1], reverse=True)

    limited_predictions = predictions[:result_num]

    recommended_books = []
    for isbn_val_set in limited_predictions:
        recommended_books.append(isbn_val_set[0])

    if result_num > len(recommended_books):
        result_num = len(recommended_books)

    # Get the top recommended books
    # recommended_books = predicted_isbns[:result_num]

    # # Get the book information from the original dataframe
    # recommended_books_info = []
    # for book in recommended_books:
    #     book_info = ratings_df.loc[ratings_df['book_isbn'] == book[0], ['book_isbn', 'book_title', 'book_author']].iloc[0]
    #     recommended_books_info.append(
    #         {'isbn': book_info['book_isbn'], 'title': book_info['book_title'], 'author': book_info['book_author'],
    #          'predicted_rating': book[1]})
    #
    # # Return the recommended books in json format
    # return json.dumps(recommended_books_info)

    # result_df = []
    #
    # for isbn in predictions:
    #     book_data = get_book(isbn)
    #     try:
    #         new_df = {int(book_data.get('isbn13')), book_data.get('bookname'), book_data.get('authors'), book_data.get('publisher'), book_data.get('class_no'), book_data.get('class_nm'), book_data.get('bookImageURL'), '0'}
    #         print(new_df)
    #         result_df.append(new_df)
    #         print('Book added successfully')
    #     except Exception as e:
    #         print('Failed to add books to book_df')
    #         return e;

    result = []
    for isbn in recommended_books:
        book_data = get_book(isbn)
        try:
            result.append({
                'isbn13': int(book_data.get('isbn13')),
                'bookname': str(book_data.get('bookname')),
                'authors': str(book_data.get('authors')),
                'publisher': str(book_data.get('publisher')),
                'class_no': str(book_data.get('class_no')),
                'class_nm': str(book_data.get('class_nm')),
                'bookImageURL': str(book_data.get('bookImageURL'))
            })
        except Exception as e:
            print('Failed to add books to book_df')
            return e;


    return json.dumps(result, ensure_ascii=False)


    # # db에서 도서 정보 불러와 df으로 할당
    # books_df = pd.read_sql_query('SELECT * FROM popular_books', conn)
    #
    # # reader object 생성
    # reader = Reader(rating_scale=(1, 5))
    #
    # # surprise Dataset에 reader 넣기
    # data = Dataset.load_from_df(ratings_df[['user_id', 'book_isbn', 'review_rating']], reader)
    #
    # # SVD model
    # svd = SVD()
    # trainset = data.build_full_trainset()
    # svd.fit(trainset)
    #
    # # 모든 책을 isbn으로 가져오기
    # all_books = list(set(ratings_df['book_isbn'].unique()).intersection(set(books_df['isbn13'].unique())))
    #
    # # 입력 받은 user에 대해 도서 isbn과 평점 리스트 생성
    # user_estimates = []
    # for book_id in all_books:
    #     user_estimates.append((book_id, svd.predict(user_id, book_id).est))
    #
    # # 평점 내림차순으로 리스트 정렬하기
    # sorted_estimates = sorted(user_estimates, key=lambda x: x[1], reverse=True)
    #
    #
    # # 위에서부터 n개 도서 가져오기
    # recommended_books = []
    #
    # if result_num > len(sorted_estimates):
    #     result_num = len(sorted_estimates)
    #
    # for i in range(result_num):
    #     isbn = sorted_estimates[i][0]
    #     book_info = books_df.loc[books_df['isbn13'] == isbn, ['isbn13', 'bookname', 'authors', 'publisher', 'class_no', 'class_nm', 'bookImageURL']].iloc[0].to_dict()
    #     recommended_books.append(book_info)
    #
    # conn.close()

    #return json.dumps(recommended_books, ensure_ascii=False)
