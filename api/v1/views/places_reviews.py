#!/usr/bin/python3
"""
Handles all default RESTFul API actions for Cities objects
"""
from flask import json, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.review import Review
from models import storage
@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_list(place_id):
    """Retrieves the list of all Places objects of a City"""
    place = storage.get(Place, place_id)
    if place:
        place_places = []
        all_reviews = storage.all(Review)
        for review in all_reviews.values():
            if review.place_id == place.id:
                place_places.append(review.to_dict())
        return jsonify(place_places)
    else:
        abort(404)
@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Place object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)
@app_views.route('/reviews/<review_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_review(review_id):
    """Delete a Place"""
    review = storage.get(Review, review_id)
    if review:
        storage.delete(review)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)

@app_views.route('/places/<place_id>/reviews', methods=['POST'],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    json_d = request.get_json()
    if not json_d:
        abort(400, "Not a JSON")
    if 'user_id' not in json_d:
        abort(400, "Missing user_id")
    user_id = storage.get(User, json_d['user_id'])
    if user_id is None:
        abort(404)
    if 'text' not in json_d:
        abort(400, "Missing text")
    review = Review(**json_d)
    review.place_id = place_id
    review.save()
    return jsonify(review.to_dict()), 201

@app_views.route('reviews/<review_id>', methods=['PUT'],
                 strict_slashes=False)
def update_review(review_id):
    "Updates a Place object"
    review = storage.get(Review, review_id)
    if not review:
        abort(404)
    json_d = request.get_json()
    if not json_d:
        abort(400, "Not a JSON")
    for key, value in json_d.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(review, key, value)
    storage.save()
    return jsonify(review.to_dict()), 200
