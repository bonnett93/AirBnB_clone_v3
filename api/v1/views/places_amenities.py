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
from models.amenity import Amenity
from os import getenv

@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_a(place_id):
    """Retrieves the list of all Reviews objects of a Place"""
    place = storage.get(Place, place_id)
    if place:
        amenities = []
        if getenv('HBNB_TYPE_STORAGE') == 'db':
            list_a = place.amenities
        else:
            list_a = place.amenity_ids
        for amenity in list_a:
            amenities.append(amenity.to_dict())
        return jsonify(amenities)
    else:
        abort(404)

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_a(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        list_a = place.amenities
    else:
        list_a = place.amenity_ids
    if amenity not in list_a:
        abort(404)
    list_a.remove(amenity)
    place.save()
    return jsonify({})

@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def create_a(place_id, amenity_id):
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        list_a = place.amenities
    else:
        list_a = place.amenity_ids
    if amenity not in list_a:
        list_a.append(amenity)
        place.save()
        return jsonify(amenity.to_dict()), 201
    return jsonify(amenity.to_dict()), 200
