from flask import current_app

from .api import Api


# Use customized version of the API extension.
api = Api(
    title="SJSU Wildfire REST API",
    version="1.0",
    # Disable the documentation from all env
    # TODO: will enable the swagger doc when adding authentication to the api url
    # doc=False
)