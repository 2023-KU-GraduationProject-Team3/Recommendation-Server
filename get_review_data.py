import requests

def get_review_data():

    try:
        response = requests.get('http://43.200.106.28:4000/review/algorithm/collab')

        json_data = response.json()

        return json_data

    except Exception as e:
        print(f"Failed to get review data from the server")
        return f"Failed to get review data from the server: {str(e)}", 400