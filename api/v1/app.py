#!/usr/bin/python3
"""starts a Flask web application"""
from os import getenv
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def close(exception):
    """call the close method"""
    storage.close()


@app.errorhandler(404)
def err(error):
    """returns a JSON-formatted 404 status code response"""
    return jsonify({"error": "Not found"})


if __name__ == "__main__":
    host = getenv('HBNB_API_HOST', '0.0.0.0')
    port = getenv('HBNB_API_PORT', 5000)
    app.run(host=host, port=port, threaded=True)
