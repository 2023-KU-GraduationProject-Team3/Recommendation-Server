from flask import Flask, request, jsonify
from algorithm.recommendation_algorithm_V5 import content_algorithm
from algorithm.recommendation_algorithm_V5 import collab_algorithm

app = Flask(__name__)

# Headers는 'Content-Type': 'application/json'
# Body는 JSON 형식으로 요청

@app.route("/api/content", methods=["GET", "POST"])
def content():
    if request.method == "POST":

        data = request.get_json()
        isbn_num = int(data.get("isbn13"))
        content_result = content_algorithm([isbn_num], 50)

        if isbn_num:
            return jsonify(content_result), 201
        else:
            return jsonify({"message": "Failed to bring data"}), 400

    elif request.method == "GET":

        isbn_num = int(request.args.get("isbn_num"))
        content_result = content_algorithm([isbn_num], 50)

        if isbn_num:
            return jsonify(content_result), 201
        else:
            return jsonify({"message": "Failed to bring data"}), 400
    else:
        return jsonify({"message": "Wrong access"}), 200

@app.route("/api/collab", methods=["GET", "POST"])
def collab():
    if request.method == "POST":

        data = request.get_json()
        user_id = int(data.get("user_id"))
        collab_result = collab_algorithm(user_id, 3)

        if user_id:
            return jsonify(collab_result), 201
        else:
            return jsonify({"message": "Failed to bring data"}), 400

    elif request.method == "GET":

        user_id = int(request.args.get("user_id"))
        collab_result = collab_algorithm(user_id, 3)

        if user_id:
            return jsonify(collab_result), 201
        else:
            return jsonify({"message": "Failed to bring data"}), 400
    else:
        return jsonify({"message": "Wrong access"}), 200

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=5000)
