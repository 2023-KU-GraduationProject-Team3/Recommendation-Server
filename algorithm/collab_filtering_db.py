#!/usr/bin/env python
# coding: utf-8

# In[9]:
import pandas as pd
import numpy as np
from surprise import Reader, Dataset, SVD
import json
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial import distance
import sqlite3
from surprise.model_selection import train_test_split

import warnings

from get_review_data import get_review_data
from get_user_info import get_user_info
from get_book import get_book


warnings.filterwarnings("ignore")

def collab_algorithm_db(user_id, result_num=10):
    review_json = get_review_data()

    my_info = get_user_info(user_id)
    my_genre = my_info['genre']
    my_age = my_info['age']
    my_gender = my_info['gender']

    ratings_df = pd.DataFrame.from_dict(review_json)

    # 새로운 사용자 데이터 생성
    new_user = pd.DataFrame({'user_id': [user_id],
                             'user_genre': [my_genre],
                             'user_age': [my_age],
                             'user_gender': [my_gender]})

    # 데이터에 새로운 사용자 추가
    updated_data = pd.concat([ratings_df, new_user], ignore_index=True)

    # 범주형 변수를 수치형으로 변환하기 위해 One-Hot Encoding
    updated_data_encoded = pd.get_dummies(updated_data, columns=['user_genre', 'user_gender'])

    # 범주형 변수와 숫자형 변수를 추출하여 각각의 데이터프레임 생성
    encoded_genre_cols = [col for col in updated_data_encoded.columns if col.startswith('user_genre_')]
    encoded_gender_cols = [col for col in updated_data_encoded.columns if col.startswith('user_gender_')]
    numeric_cols = ['user_age']
    encoded_genre_data = updated_data_encoded[encoded_genre_cols]
    encoded_gender_data = updated_data_encoded[encoded_gender_cols]
    numeric_data = updated_data_encoded[numeric_cols]

    # Min-Max 스케일링을 통해 숫자형 변수 정규화
    scaler = MinMaxScaler()
    numeric_data_scaled = scaler.fit_transform(numeric_data)

    # 정규화된 숫자형 변수와 범주형 변수 데이터를 병합
    merged_data = pd.concat([pd.DataFrame(numeric_data_scaled, columns=numeric_cols),
                             encoded_genre_data, encoded_gender_data], axis=1)

    # 코사인 유사도 계산
    similarity_matrix = cosine_similarity(merged_data)

    # 새로운 사용자와 각 데이터 포인트의 유사도 추출
    new_user_similarity = similarity_matrix[-1, :-1]

    # 유사도 기준으로 데이터 정렬
    sorted_indices = new_user_similarity.argsort()[::-1]

    # 평점이 4.0 이상인 ISBN 추출
    recommended_books = []
    for index in sorted_indices:
        if ratings_df['review_rating'].iloc[index] >= 4.0:
            recommended_books.append(ratings_df['book_isbn'].iloc[index])



    if result_num > len(recommended_books):
        result_num = len(recommended_books)

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
