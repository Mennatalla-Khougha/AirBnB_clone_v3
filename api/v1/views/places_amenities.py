#!/usr/bin/python3
"""review route"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.place import Place
from models.amenity import Amenity
from os import getenv


@app_views.route(
        '/places/<place_id>/amenities',
        strict_slashes=False
    )
def amenity_from_place_id(place_id):
    """Retrieves the list of all amenities objects of a place"""
    place = storage.get(Place, place_id)
    if place:
        amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(amenities)
    abort(404)


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['DELETE'],
        strict_slashes=False
    )
def delete_amenity2(place_id, amenity_id):
    """Returns an empty dictionary with the status code 200"""
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if amenity.place_id != place_id:
        abort(404)

    place.amenity.delete()
    storage.save()
    return (jsonify({}))


@app_views.route(
        '/places/<place_id>/amenities/<amenity_id>',
        methods=['POST'],
        strict_slashes=False
    )
def post_amenity2(place_id, amenity_id):
    """Creates an amenity"""

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if amenity.place_id == place_id:
        return jsonify(amenity.to_dict())

    place.amenities.append(amenity)
    place.save()
    return jsonify(amenity.to_dict()), 201
