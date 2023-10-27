#!/usr/bin/python3
"""cities route"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', strict_slashes=False)
def city_from_state_id(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state:
        cities = [city.to_dict() for city in state.cities]
        return jsonify(cities)
    abort(404)


@app_views.route('/cities/<city_id>', strict_slashes=False)
def city_with_id(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
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
        return jsonify({"error": "Not a JSON"}), 400

    state = storage.get(State, state_id)
    if not state:
        abort(404)

    data = request.get_json()
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    city = City(**data)
    city.state_id = state_id
    city.save()
    return jsonify(city.to_dict()), 201


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
        return jsonify({"error": "Not a JSON"}), 400

    cities = request.get_json()
    for key, value in cities.items():
        if key not in ('id', 'state_id', 'created_at', 'updated_at'):
            setattr(data, key, value)
    data.save()
    return jsonify(data.to_dict()), 200
