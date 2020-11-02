import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resource={r"/*": {"origins": "*"}})


@app.route("/", methods=["GET"])
def get():
    return jsonify(name="hello world")


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

if __name__ == "__main__":
    main()
