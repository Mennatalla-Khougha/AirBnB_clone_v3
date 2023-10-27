#!/usr/bin/python3
"""states routes"""
from api.v1.views import app_views
from flask import Flask, abort, Response, jsonify, request
from models import storage
from models.state import State
import json


@app_views.route('/states', strict_slashes=False)
def states():
    """Retrieves the list of all State objects"""
    states = []
    for state in storage.all(State).values():
        states.append(state.to_dict())
    formatted_json = json.dumps(states, indent=2) + '\n'
    result = Response(formatted_json, content_type='application/json')
    return result


@app_views.route('/states/<state_id>', strict_slashes=False)
def states_with_id(state_id):
    """Retrieves the list of all State objects"""
    state = storage.get(State, state_id)
    if state:
        formatted_json = json.dumps(state.to_dict(), indent=2) + '\n'
        result = Response(formatted_json, content_type='application/json')
        return result
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
        formatted_json = json.dumps({"error": "Not a JSON"}, indent=2) + '\n'
        result = Response(formatted_json, content_type='application/json')
        return result, 400

    data = request.get_json()
    if 'name' not in data:
        formatted_json = json.dumps({"error": "Missing name"}, indent=2) + '\n'
        result = Response(formatted_json, content_type='application/json')
        return result, 400

    state = State(data)
    formatted_json = json.dumps(state.to_dict(), indent=2) + '\n'
    result = Response(formatted_json, content_type='application/json')
    return result, 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_route(state_id):
    """Returns the State object with the status code 200"""
    data = storage.get(State, state_id)
    if data is None:
        abort(404)

    if not request.is_json:
        formatted_json = json.dumps({"error": "Not a JSON"}, indent=2) + '\n'
        result = Response(formatted_json, content_type='application/json')
        return result, 400

    states = request.get_json()
    for key, value in states.items():
        if key not in ('id', 'created_st', 'updated_at'):
            setattr(data, key, value)
    data.save()
    formatted_json = json.dumps(data.to_dict(), indent=2) + '\n'
    result = Response(formatted_json, content_type='application/json')
    return result, 200
