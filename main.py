from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class MainClass(Resource):
    def get(self):
        return {'data': 'hello world'}


api.add_resource(MainClass, "/")

if __name__ == '__main__':
    app.run(debug=True)
