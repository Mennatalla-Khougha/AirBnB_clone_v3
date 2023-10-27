#!/usr/bin/python3
"""users route"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.user import User


@app_views.route(
    '/users',
    strict_slashes=False
    )
def all_users():
    """Retrieves the list of all User objects"""
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route(
    '/users/<user_id>',
    strict_slashes=False
    )
def user_with_id(user_id):
    """Retrieves the specified User object"""
    user = storage.get(User, user_id)
    if user:
        return jsonify(user.to_dict())
    abort(404)


@app_views.route(
    '/users/<user_id>',
    methods=['DELETE'],
    strict_slashes=False
    )
def delete_user(user_id):
    """Returns an empty dictionary with the status code 200"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    user.delete()
    storage.save()
    return (jsonify({}))


@app_views.route(
    '/users',
    methods=['POST'],
    strict_slashes=False
    )
def post_user():
    """Returns the new user with the status code 201"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if 'email' not in data:
        return jsonify({"error": "Missing email"}), 400

    if 'password' not in data:
        return jsonify({"error": "Missing password"}), 400

    user = User(**data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route(
    '/users/<user_id>',
    methods=['PUT'],
    strict_slashes=False
    )
def put_user(user_id):
    """Returns the User object with the status code 200"""
    data = storage.get(User, user_id)
    if data is None:
        abort(404)

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    users = request.get_json()
    for key, value in users.items():
        if key not in ('id', 'email', 'created_at', 'updated_at'):
            setattr(data, key, value)
    data.save()
    return jsonify(data.to_dict()), 200
