import settings

from . import ml_api
from flask_restplus import Resource

@ml_api.route("/")
class MachineLearningModel(Resource):

    def get(self):
        print("Machine learning endpoint")

        return "Success"
