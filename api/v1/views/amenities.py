#!/usr/bin/python3
"""cities route"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = []
    for amenity in storage.all(Amenity).values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>', strict_slashes=False)
def amenity_with_id(amenity_id):
    """Retrieves the list of all amenity objects"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity:
        return jsonify(amenity.to_dict())
    abort(404)


@app_views.route(
        'amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False
    )
def delete_amenity(amenity_id):
    """Returns an empty dictionary with the status code 200"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a amenity"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400


    amenity = Amenity(**data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route(
        'amenities/<amenity_id>',
        methods=['PUT'],
        strict_slashes=False
    )
def put_amenity(amenity_id):
    """Returns the amenity object with the status code 200"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    for key, value in data.items():
        if key not in ('id', 'created_st', 'updated_at'):
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200
