#!/usr/bin/python3
"""cities route"""
from api.v1.views import app_views
from flask import Flask, abort, Response, jsonify, request
from models import storage
from models.state import State
from models.city import City
import json


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def city_from_state_id(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        formatted_json = json.dumps(cities, indent=2) + '\n'
        result = Response(formatted_json, content_type='application/json')
        return result
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city_with_id(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city:
        formatted_json = json.dumps(city.to_dict(), indent=2) + '\n'
        result = Response(formatted_json, content_type='application/json')
        return result
    abort(404)


@app_views.route(
        'cities/<city_id>',
        methods=['DELETE'],
        strict_slashes=False
    )
def delete_city(city_id):
    """Returns an empty dictionary with the status code 200"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    city.delete()
    storage.save()
    return (jsonify({}))


@app_views.route(
    '/states/<state_id>/cities',
    methods=['POST'],
    strict_slashes=False
    )
def post_city(state_id):
    """Creates a City"""
    if not request.is_json:
        formatted_json = json.dumps({"error": "Not a JSON"}, indent=2) + '\n'
        result = Response(formatted_json, content_type='application/json')
        return result, 400

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if 'name' not in data:
        formatted_json = json.dumps({"error": "Missing name"}, indent=2) + '\n'
        result = Response(formatted_json, content_type='application/json')
        return result, 400

    city = City(**data)
    city.state_id = state_id
    storage.save()
    formatted_json = json.dumps(city.to_dict(), indent=2) + '\n'
    result = Response(formatted_json, content_type='application/json')
    return result, 201


@app_views.route(
    'cities/<city_id>',
    methods=['PUT'],
    strict_slashes=False
    )
def put_city(city_id):
    """Returns the city object with the status code 200"""
    data = storage.get(City, city_id)
    if data is None:
        abort(404)

    if not request.is_json:
        formatted_json = json.dumps({"error": "Not a JSON"}, indent=2) + '\n'
        result = Response(formatted_json, content_type='application/json')
        return result, 400

    cities = request.get_json()
    for key, value in cities.items():
        if key not in ('id', 'state_id', 'created_st', 'updated_at'):
            setattr(data, key, value)
    data.save()
    formatted_json = json.dumps(data.to_dict(), indent=2) + '\n'
    result = Response(formatted_json, content_type='application/json')
    return result, 200
