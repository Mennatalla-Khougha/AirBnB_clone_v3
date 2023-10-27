#!/usr/bin/python3
"""review route"""
from api.v1.views import app_views
from flask import Flask, abort, jsonify, request
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route(
    '/places/<place_id>/reviews',
    strict_slashes=False
    )
def reviews_from_place_id(place_id):
    """Retrieves the list of all review objects of a place"""
    place = storage.get(Place, place_id)
    if place:
        reviews = [review.to_dict() for review in place.reviews]
        return jsonify(reviews)
    abort(404)


@app_views.route(
    '/reviews/<review_id>',
    strict_slashes=False)
def review_with_id(review_id):
    """Retrieves a review object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    abort(404)


@app_views.route(
        '/reviews/<review_id>',
        methods=['DELETE'],
        strict_slashes=False
    )
def delete_review(review_id):
    """Returns an empty dictionary with the status code 200"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return (jsonify({}))


@app_views.route(
        '/places/<place_id>/reviews',
        methods=['POST'],
        strict_slashes=False
    )
def post_review(place_id):
    """Creates a review"""
    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    place = storage.get(Place, place_id)
    if not place:
        abort(404)

    data = request.get_json()
    if 'user_id' not in data:
        return jsonify({"error": "Missing user_id"}), 400

    user = storage.get(User, data['user_id'])
    if not user:
        abort(404)

    if 'text' not in data:
        return jsonify({"error": "Missing text"}), 400

    review = Review(**data)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201


@app_views.route(
        '/reviews/<review_id>',
        methods=['PUT'],
        strict_slashes=False
    )
def put_review(review_id):
    """Returns the review object with the status code 200"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)

    if not request.is_json:
        return jsonify({"error": "Not a JSON"}), 400

    data = request.get_json()
    for key, value in data.items():
        if key not in (
            'id',
            'user_id',
            'place_id',
            'created_at',
            'updated_at'
        ):
            setattr(review, key, value)
    review.save()
    return jsonify(review.to_dict()), 200
