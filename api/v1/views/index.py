#!/usr/bin/python3
from api.v1.views import app_views
from flask import Flask, jsonify


@app_views.route('/status')
def status():
    """displays a API page"""
    response = {"status": "OK"}
    return jsonify(response)
