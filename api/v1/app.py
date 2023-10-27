#!/usr/bin/python3
"""starts a Flask web application"""
from os import getenv
from flask import Flask, Response
from models import storage
from api.v1.views import app_views
import json
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """call the close method"""
    storage.close()


@app.errorhandler(404)
def err(error):
    """returns a JSON-formatted 404 status code response"""
    response = {"error": "Not found"}
    formatted_json = json.dumps(response, indent=2) + '\n'
    result = Response(formatted_json, content_type='application/json')
    return result


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
