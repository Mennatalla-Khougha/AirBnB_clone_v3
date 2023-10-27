#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, Response
from models import storage
import json


@app_views.route('/status')
def status():
    """displays a API page"""
    formatted_json = json.dumps({"status": "OK"}, indent=2) + '\n'
    result = Response(formatted_json, content_type='application/json')
    return result


@app_views.route('/stats')
def stats():
    """ retrieves the number of each objects by type"""
    response = {
        "amenites": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "review": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    formatted_json = json.dumps(response, indent=2) + '\n'
    result = Response(formatted_json, content_type='application/json')
    return result
