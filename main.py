from flask import Flask, request, jsonify
from algorithm.content_filtering_db import content_algorithm_db
from algorithm.collab_filtering_db import collab_algorithm_db
from update_popular_books import update_popular_books

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

popular_books_total_num = update_popular_books(False)
#print(content_algorithm_db([9791130627984, 9791160022490], 10))
print(collab_algorithm_db("0a547b05-d29b-49b5-8a37-f44684c1a332", 5))

# Headers는 'Content-Type': 'application/json'
# Body는 JSON 형식으로 요청

@app.route("/api/content", methods=["GET", "POST"])
def content():

    if request.method == "POST":
        try:
            isbns = request.json['isbn']
            result_num = request.json.get('result_num', 10)

        except KeyError:
            return jsonify({'error': 'Invalid request. Parameter "isbn" missing in request body.'}), 400

        content_result = content_algorithm_db(isbns, result_num)

        return content_result, 201

    else:
        return jsonify({"message": "Wrong access"}), 200

@app.route("/api/collab", methods=["GET", "POST"])
def collab():
    if request.method == "POST":
        try:
            user_id = request.json['user_id']
            result_num = request.json.get('result_num', 10)

        except KeyError:
            return jsonify({'error': 'Invalid request. Parameter "isbn" missing in request body.'}), 400

        collab_result = collab_algorithm_db(user_id, result_num)

        return collab_result, 201

    else:
        return jsonify({"message": "Wrong access"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
