from flask import Flask, request, jsonify
from algorithm.recommendation_algorithm_V5 import content_algorithm
from algorithm.recommendation_algorithm_V5 import collab_algorithm

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

# Headers는 'Content-Type': 'application/json'
# Body는 JSON 형식으로 요청

@app.route("/api/content", methods=["GET", "POST"])
def content():
    if request.method == "POST":

        data = request.get_json()
        isbn_num = int(data.get("isbn13"))
        content_result = content_algorithm([isbn_num], 10)

        if isbn_num:
            return content_result, 201
        else:
            return jsonify({"message": "Failed to bring data"}), 400

    elif request.method == "GET":
        isbn_num = -1
        content_result = -1

        if len(request.args) != 0 and request.args.get("isbn_num") is not None:
            isbn_num = int(request.args.get("isbn_num"))
            content_result = content_algorithm([isbn_num], 50)

        if isbn_num >= 0:
            return content_result, 201
        elif isbn_num < 0:
            return jsonify("isbn_num 값을 파라미터로 넘기세요."), 201
        else:
            return jsonify({"message": "Failed to bring data"}), 400
    else:
        return jsonify({"message": "Wrong access"}), 200

@app.route("/api/collab", methods=["GET", "POST"])
def collab():
    if request.method == "POST":

        data = request.get_json()
        user_id = int(data.get("user_id"))
        collab_result = collab_algorithm(user_id, 5)

        if user_id:
            return collab_result, 201
        else:
            return jsonify({"message": "Failed to bring data"}), 400

    elif request.method == "GET":

        user_id = int(request.args.get("user_id"))
        collab_result = collab_algorithm(user_id, 3)

        if user_id:
            return collab_result, 201
        else:
            return jsonify({"message": "Failed to bring data"}), 400
    else:
        return jsonify({"message": "Wrong access"}), 200

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port=5000, debug=True)
