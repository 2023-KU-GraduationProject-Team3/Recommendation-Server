import requests
import json
import xmltodict

def get_book(isbn):
    url = "http://data4library.kr/api/srchDtlList?authKey=32bb82a55e2ccb6dd8baec16309bed7ecc2985e9a07e83dc18b5037179636d55&isbn13="+str(isbn)+"&loaninfoYN=Y"
    headers = {'Content-Type': 'application/json', 'charset': 'UTF-8', 'Accept': '*/*'}
    response = requests.get(url, headers=headers)

    xml_data = xmltodict.parse(response.text)

    jsonData = json.dumps(xml_data, ensure_ascii=False)

    jsonObject = json.loads(jsonData)

    result = jsonObject.get("response").get("detail").get("book")

    return result