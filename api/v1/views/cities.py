#!/usr/bin/python3
"""
Handles all default RESTFul API actions for Cities objects
"""

from flask import json, jsonify, abort, request
from api.v1.views import app_views
from models.state import State
from models.city import City
from models import storage


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_city_list(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state:
        state_cities = []
        all_cities = storage.all(City)
        for city in all_cities.values():
            if city.state_id == state.id:
                state_cities.append(city.to_dict())
        return jsonify(state_cities)
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city:
        return jsonify(city.to_dict())
    else:
        abort(404)


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Delete a city"""
    city = storage.get(City, city_id)
    if city:
        storage.delete(city)
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    json_d = request.get_json()
    if not json_d:
        abort(400, "Not a JSON")
    if 'name' not in json_d:
        abort(400, "Missing name")

    new_city = City(**json_d)
    new_city.state_id = state_id
    new_city.save()
    return jsonify(new_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    "Updates a City object"
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    json_d = request.get_json()
    if not json_d:
        abort(400, "Not a JSON")
    for key, value in json_d.items():
        if key not in ['id', 'state_id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
