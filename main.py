from flask import Flask, request, jsonify
from algorithm.recommendation_algorithm_V5 import recommend_books

app = Flask(__name__)

@app.route("/api", methods=["GET", "POST"])

# Headers는 'Content-Type': 'application/json'
# Body는 JSON 형식으로 요청

def recommendation():

    if request.method == "POST":
        data = request.get_json()
        isbn_num = int(data.get("isbn13"))
        result = recommend_books([isbn_num], 50)

        if isbn_num:
            return jsonify(result), 201
        else:
            return jsonify({"message": "Error"}), 400
    else:
        return jsonify({"message": "Success! Request method is GET!"}), 200

if __name__ == "__main__":
    app.run(host = 'http://localhost/', port=8080)
