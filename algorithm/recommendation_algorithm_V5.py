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

def collab_algorithm(user_id, num_books=10):
    # rating csv 파일 일기
    ratings_df = pd.read_csv('res/ratings_final_ISBN3.csv')

    # 도서 csv 파일 일기
    books_df = pd.read_csv('res/popular_books_ISBN3.csv')

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
    for i in range(num_books):
        isbn = sorted_estimates[i][0]
        bookname = books_df.loc[books_df['isbn13'] == isbn, 'bookname'].iloc[0]
        recommended_books.append({"isbn13": int(isbn), "bookname": str(bookname)})

    return json.dumps(recommended_books, ensure_ascii=False)


#print("----- 협업 필터링 결과 ------")
#print(str(collab_algorithm(2, 3)))  # 협업 필터링 최종 결과
#print("-----------------------------")



def content_algorithm(favorites, n):

    # CSV 파일 불러오기
    df = pd.read_csv("res/book_df.csv")

    # 작가 이름이 완전히 같은지 체크
    df["same_author"] = df.duplicated(subset="authors", keep=False)

    # 작가 이름이 완전히 같지 않으면 제목과 출판사, 장르만 고려하기
    df["content"] = df[["bookname", "publisher"]].apply(lambda x: " ".join(x), axis=1)
    df.loc[df["same_author"], "content"] = df.loc[df["same_author"], "content"] + " " + df.loc[df["same_author"], "authors"]


    # TfidfVectorizer 생성
    vectorizer = TfidfVectorizer(stop_words="english")

    # 모든 요소에 대해 Tf-idf vectorization 적용
    content_matrix = vectorizer.fit_transform(df["content"])

    # 코사인 유사도 구하기
    cosine_sim = cosine_similarity(content_matrix)


    # favorites 책들을 담을 빈 배열 indices 생성
    indices = []

    # favorites 책에서
    for isbn in favorites:
        # isbn 값과 일치하는 인덱스 가져오기
        idx = df[df['isbn13'] == isbn].index[0]
        # indices에 그 책 추가
        indices.append(idx)


    # favorites 책으로 책의 유사도 점수 목록 만들기
    sim_scores = [list(enumerate(cosine_sim[i])) for i in indices]
    sim_scores = [item for sublist in sim_scores for item in sublist]

    # 유사도 점수가 높은 수능로 정렬하기
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 유사도 높은 순에서 가장 유사도 높은 len(favorites) 제거하고 n개 가져오기
    top_n = [i[0] for i in sim_scores[len(favorites) : n + len(favorites)]]

    # 가장 유사도 높은 n개의 책 가져오기
    return df.iloc[top_n].to_json(orient="index", force_ascii=False)


# 함수 호출
# print(recommend_books([9788954622035], 50))


# In[ ]:




