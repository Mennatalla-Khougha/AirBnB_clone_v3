#!/usr/bin/python3
"""states routes"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.state import State


@app_views.route('/states', strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    return jsonify(states)


@app_views.route('/states/<state_id>', strict_slashes=False)
def states_with_id(state_id):
    """Retrieves the list of all State objects"""
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    abort(404)


@app_views.route(
        '/states/<state_id>',
        methods=['DELETE'],
        strict_slashes=False
    )
def delete_route(state_id):
    """Returns an empty dictionary with the status code 200"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_route():
    """Returns the new State with the status code 201"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    state = State(**data)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_route(state_id):
    """Returns the State object with the status code 200"""
    data = storage.get(State, state_id)
    if data is None:
        abort(404)

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    states = request.get_json()
    for key, value in states.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(data, key, value)
    data.save()
    return jsonify(data.to_dict()), 200
