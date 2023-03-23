import pandas as pd
import requests
from datetime import datetime
from xml.etree.ElementTree import parse

def write_csv():

    today = str(datetime.today().strftime("%Y-%m-%d"))

    url = "http://data4library.kr/api/loanItemSrch?authKey=32bb82a55e2ccb6dd8baec16309bed7ecc2985e9a07e83dc18b5037179636d55&startDt=2023-01-01&endDt=" + today
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    response = requests.get(url, headers=headers)
    xml_data = response.text

    ### xml을 DataFrame으로 변환하기 ###
    from os import name
    import xml.etree.ElementTree as et
    import pandas as pd
    import bs4
    from lxml import html
    from urllib.parse import urlencode, quote_plus, unquote

    # bs4 사용하여 item 태그 분리

    xml_obj = bs4.BeautifulSoup(xml_data, 'lxml-xml')
    rows = xml_obj.findAll('doc')
    print(rows)
    """
    # 컬럼 값 조회용
    columns = rows[0].find_all()
    print(columns)
    """

    # 각 행의 컬럼, 이름, 값을 가지는 리스트 만들기
    row_list = []  # 행값
    column_list = []  # 열이름값
    value_list = []  # 데이터값

    # xml 안의 데이터 수집
    for i in range(0, len(rows)):
        columns = rows[i].find_all()
        # 첫째 행 데이터 수집
        for j in range(0, len(columns)):
            if i == 0:
                # 컬럼 이름 값 저장
                column_list.append(columns[j].name)
            # 컬럼의 각 데이터 값 저장
            value_list.append(columns[j].text)
        # 각 행의 value값 전체 저장
        row_list.append(value_list)
        # 데이터 리스트 값 초기화
        value_list = []

    # xml값 DataFrame으로 만들기
    book_df = pd.DataFrame(row_list, columns=column_list)
    ###assertion error의 경우###
    ###corona_df = pd.DataFrame(row_list)
    print(book_df.head(19))

    # DataFrame CSV 파일로 저장
    book_df.to_csv('./res/book_df.csv', encoding='utf-8-sig')