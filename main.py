from flask import Flask, request, jsonify
# from algorithm.recommendation_algorithm_V5 import content_algorithm
# from algorithm.recommendation_algorithm_V5 import collab_algorithm
from algorithm.content_filtering import content_algorithm
from algorithm.collab_filtering import collab_algorithm
from algorithm.content_filtering_db import content_algorithm_db
from algorithm.collab_filtering_db import collab_algorithm_db
from writeCSV import write_csv
from get_book import get_book
from operation_to_db import add_book_to_db, delete_book_from_db
from update_popular_books import update_popular_books

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

popular_books_total_num = update_popular_books(False)
#print(get_book(9791130627984))
#print(content_algorithm_db([9791130627984, 9791160022490], 10))
print(collab_algorithm_db(2, 5))

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

    # elif request.method == "GET":
    #     isbn = -1
    #     content_result = -1
    #     result_num = 10
    #
    #     if request.args.get("result_num") is not None:
    #         result_num = int(request.args.get("result_num"))
    #
    #     if len(request.args) != 0 and request.args.get("isbn") is not None:
    #         isbn = int(request.args.get("isbn"))
    #         content_result = content_algorithm([isbn], result_num)
    #
    #     if isbn >= 0:
    #         return content_result, 201
    #     elif isbn < 0:
    #         return jsonify("isbn 값을 파라미터로 넘기세요."), 201
    #     else:
    #         return jsonify({"message": "Failed to bring data"}), 400
    else:
        return jsonify({"message": "Wrong access"}), 200

@app.route("/api/collab", methods=["GET", "POST"])
def collab():
    if request.method == "POST":

        try:
            user_id = int(request.json['user_id'])
            result_num = request.json.get('result_num', 10)

        except KeyError:
            return jsonify({'error': 'Invalid request. Parameter "isbn" missing in request body.'}), 400

        collab_result = collab_algorithm_db(user_id, result_num)

        # data = request.get_json()
        # user_id = int(data.get("user_id"))
        # collab_result = collab_algorithm(user_id, 5)

        return collab_result, 201

    # elif request.method == "GET":
    #
    #     user_id = -1
    #     collab_result = -1
    #     result_num = 10
    #
    #     if request.args.get("result_num") is not None:
    #         result_num = int(request.args.get("result_num"))
    #
    #     if len(request.args) != 0 and request.args.get("user_id") is not None:
    #         user_id = int(request.args.get("user_id"))
    #         collab_result = collab_algorithm(user_id, result_num)
    #
    #     if user_id >= 0:
    #         return collab_result, 201
    #     elif user_id < 0:
    #         return jsonify("user_id 값을 파라미터로 넘기세요."), 201
    #     else:
    #         return jsonify({"message": "Failed to bring data"}), 400
    else:
        return jsonify({"message": "Wrong access"}), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
