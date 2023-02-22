#!/usr/bin/env python
# coding: utf-8

# In[9]:
import numpy as np
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

from scipy.sparse.linalg import svds
import warnings


warnings.filterwarnings("ignore")

def collab_algorithm(user_id, num_recommendations=5):
    df_ratings = pd.read_csv('res/ratings_final_ISBN3.csv')  # 유저랑 동일한 성별 및 비슷한 나이대로 필터링 하고난 ratings.csv 사용
    df_books = pd.read_csv('res/popular_books_ISBN3.csv')

    df_user_movie_ratings = df_ratings.pivot(
        index='userId',
        columns='isbn13',
        values='rating'
    ).fillna(0)

    # df_user_movie_ratings.head(3)
    # 사용자 - 도서 pivot table 제작

    # matrix는 pivot_table 값을 numpy matrix로 만든 것
    matrix = df_user_movie_ratings.values

    # user_ratings_mean은 사용자의 평균 평점 (평을 안 남긴 유저들도 있기 때문)
    user_ratings_mean = np.mean(matrix, axis=1)

    # R_user_mean : 사용자-도서에 대해 사용자 평균 평점을 뺀 것.
    matrix_user_mean = matrix - user_ratings_mean.reshape(-1, 1)
    matrix

    pd.DataFrame(matrix_user_mean, columns=df_user_movie_ratings.columns).head()

    # svd 를 이용해 matrix factorization
    # svd : 특이값 분해
    # -> m * n 크기의 데이터 행렬 A를 분해

    # scipy에서 제공해주는 svd.
    # U 행렬, sigma 행렬, V 전치 행렬을 반환.

    U, sigma, Vt = svds(matrix_user_mean, k=5)

    # print(U.shape)
    # print(sigma.shape)
    # print(Vt.shape)
    sigma = np.diag(sigma)
    sigma.shape
    sigma[0]
    sigma[1]
    # 0 이 포함된 대칭행렬로 변환하기 위해 numpy의 diag를 이용함

    # U, Sigma, Vt의 내적을 수행하면, 다시 원본 행렬로 복원이 된다.
    # 내적 => np.dot(np.dot(U, sigma), Vt) 수행
    # 거기에 + 사용자 평균 rating을 적용한다.
    svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

    df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns=df_user_movie_ratings.columns)
    df_svd_preds.head()

    df_svd_preds.shape

    return calculate(df_svd_preds, user_id, df_books, df_ratings, num_recommendations)



# 1. 행렬 분해를 활용한 협업 필터링 #
# 사용자 개인 도서 히스토리를 기반으로 도서추천 #

def calculate(df_svd_preds, user_id, ori_books_df, ori_ratings_df, num_recommendations=5):

    # 현재는 index로 적용이 되어있으므로 user_id - 1을 해야함.
    user_row_number = user_id - 1

    # 최종적으로 만든 pred_df에서 사용자 index에 따라 도서 데이터 정렬 -> 도서 평점이 높은 순으로 정렬 됌
    sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(ascending=False)

    # 원본 평점 데이터에서 user id에 해당하는 데이터를 뽑아낸다.
    user_data = ori_ratings_df[ori_ratings_df.userId == user_id]

    # 위에서 뽑은 user_data와 원본 도서 데이터를 합친다.
    user_history = user_data.merge(ori_books_df, on='isbn13').sort_values(['rating'], ascending=False)

    # 원본 도서 데이터에서 사용자가 본 도서 데이터를 제외한 데이터를 추출
    recommendations = ori_books_df[~ori_books_df['isbn13'].isin(user_history['isbn13'])]
    # 사용자의 도서 평점이 높은 순으로 정렬된 데이터와 위 recommendations을 합친다.
    recommendations = recommendations.merge(pd.DataFrame(sorted_user_predictions).reset_index(), on='isbn13')
    # 컬럼 이름 바꾸고 정렬해서 return
    recommendations = recommendations.rename(columns={user_row_number: 'Predictions'}).sort_values('Predictions',
                                                                                                   ascending=False).iloc[
                      :num_recommendations, :]

    already_rated = user_history
    predictions = recommendations

    # 원하는 유저의 userId(인덱스) 넣어주기
    already_rated.head(10)

    return predictions




print("----- 협업 필터링 결과 ------")
print(collab_algorithm(7, 3))  # 협업 필터링 최종 결과
print("-----------------------------")
print()
print()



def content_algorithm(favorites, n):

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




