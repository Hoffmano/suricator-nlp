import os
from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource

app = Flask(__name__)

# cors = CORS(app, resource={r"/*": {"origins": "*"}})

api = Api(app)


class Main(Resource):
    def get(self):
        return {"name": "api"}


# @ app.route("/", methods=['GET'])
# def index():
#     return "<h1>Testando deploy GitHub x Heroku </h1>"


def main():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)


api.add_resource(Main, "/")

if __name__ == "__main__":
    main()
