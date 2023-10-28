#!/usr/bin/python3
"""cities route"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', strict_slashes=False)
def places_from_city_id(city_id):
    """Retrieves the list of all Place objects of a City"""
    city = storage.get(City, city_id)
    if city:
        places = [place.to_dict() for place in city.places]
        return jsonify(places)
    abort(404)


@app_views.route('/places/<place_id>', strict_slashes=False)
def place_with_id(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    abort(404)


@app_views.route(
        '/places/<place_id>',
        methods=['DELETE'],
        strict_slashes=False
    )
def delete_place(place_id):
    """Returns an empty dictionary with the status code 200"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}))


@app_views.route(
        '/cities/<city_id>/places',
        methods=['POST'],
        strict_slashes=False
    )
def post_place(city_id):
    """Creates a City"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    city = storage.get(City, city_id)
    if not city:
        abort(404)

    data = request.get_json()

    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'name' not in data:
        return jsonify({"error": "Missing name"}), 400

    place = Place(**data)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route(
        '/places/<place_id>',
        methods=['PUT'],
        strict_slashes=False
    )
def put_place(place_id):
    """Returns the place object with the status code 200"""
    data = storage.get(Place, place_id)
    if data is None:
        abort(404)

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    places = request.get_json()
    for key, value in places.items():
        if key not in ('id', 'user_id', 'city_it', 'created_at', 'updated_at'):
            setattr(data, key, value)
    data.save()
    return jsonify(data.to_dict()), 200


@app_views.route(
        '/places_search',
        methods=['POST'],
        strict_slashes=False
    )
def post_place_2():
    """Creates a City"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()

    if not data or not (data.get('state') or data.get('cities')):
        places = storage.all(Place).values()

    else:
        places = {}
        states = data.get('states')
        if states:
            for state in states:
                for city in state.cities:
                    places[city.name] = city.places

        cities = data.get('cities')
        if cities:
            for city in cities:
                places[city.name] = city.places

        tmp = []
        for city in places.values():
            for place in city:
                tmp.append(place)
        places = tmp

    amenities = data.get('amenities')
    if amenities:
        result = []
        for place in places:
            amenity_ids = [amenity.id for amenity in place.amenities]
            if all(menity in amenity_ids for menity in amenities):
                result.append(place)
    else:
        result = places

    return jsonify([place.to_dict() for place in result])
