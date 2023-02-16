#!/usr/bin/env python
# coding: utf-8

# In[9]:


import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer


def recommend_books(favorites, n):

    # CSV 파일 불러오기
    df = pd.read_csv("res/popular_books_ISBN3.csv")

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




