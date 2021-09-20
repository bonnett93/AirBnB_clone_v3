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
from models import storage


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places_list(city_id):
    """Retrieves the list of all Places objects of a City"""
    city = storage.get(City, city_id)
    if city:
        city_places = []
        all_places = storage.all(Place)
        for place in all_places.values():
            if place.city_id == city.id:
                city_places.append(place.to_dict())
        return jsonify(city_places)
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id):
    """Retrieves a Place object"""
    place = storage.get(Place, place_id)
    if place:
        return jsonify(place.to_dict())
    else:
        abort(404)


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Delete a Place"""
    place = storage.get(Place, place_id)
    if place:
        storage.delete(place)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a place"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    json_d = request.get_json()
    if not json_d:
        abort(400, "Not a JSON")
    if 'user_id' not in json_d:
        abort(400, "Missing user_id")
    user_id = storage.get(User, json_d['user_id'])
    if user_id is None:
        abort(404)
    if 'name' not in json_d:
        abort(400, "Missing name")

    place = Place(**json_d)
    place.city_id = city_id
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a Place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    json_d = request.get_json()
    if not json_d:
        abort(400, "Not a JSON")
    for key, value in json_d.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200
