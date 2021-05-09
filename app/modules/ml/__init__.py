from flask_restplus import Namespace

from app.extensions import api


ml_api = Namespace(
    "ml", path="/ml",
    description="Endpoint for machine learning model"
)

def init_app(app):
    from . import resources
    api.add_namespace(ml_api)

