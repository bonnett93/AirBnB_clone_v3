#!/usr/bin/python3
"""
Handles all default RESTFul API actions for Reviews objects
"""

from flask import jsonify, abort, request
from api.v1.views import app_views
from models.place import Place
from models.user import User
from models.review import Review
from models import storage


@app_views.route('/places/<place_id>/reviews', methods=['GET'],
                 strict_slashes=False)
def get_review_list(place_id):
    """Retrieves the list of all Reviews objects of a Place"""
    place = storage.get(Place, place_id)
    if place:
        place_reviews = []
        all_reviews = storage.all(Review)
        for review in all_reviews.values():
            if review.place_id == place.id:
                place_reviews.append(review.to_dict())
        return jsonify(place_reviews)
    else:
        abort(404)


@app_views.route('/reviews/<review_id>', methods=['GET'], strict_slashes=False)
def get_review(review_id):
    """Retrieves a Review object"""
    review = storage.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    else:
        abort(404)
