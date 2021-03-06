from nlp import difficulty
import os
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route("/", methods=["POST"])
@cross_origin()
def post():

    song = request.get_json()

    print(song["lyrics"])

    response = jsonify(
        difficulty = difficulty(song)
    )

    return response


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


if __name__ == "__main__":
    main()
