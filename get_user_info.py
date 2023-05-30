import requests

def get_user_info(userId):

    try:
        response = requests.get('http://43.200.106.28:4000/user/user-info/'+userId)

        json_data = response.json()

        return json_data

    except Exception as e:
        print(f"Failed to get user information from the server")
        return f"Failed to get user information from the server: {str(e)}", 400