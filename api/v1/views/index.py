#!/usr/bin/python3
"""status and stats routes"""
from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
import json


@app_views.route('/status')
def status():
    """displays a API page"""
    return jsonify({"status": "OK"})


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
    return jsonify(response)
