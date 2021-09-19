#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = []
    for amenity in storage.all('Amenity').values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def amenity_id(amenity_id):
    """Retrieves a Amenity object by id"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    else:
        return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    storage.delete(amenity)
    storage.save()
    empty = jsonify({})
    return (empty), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """Creates a amenity"""
    json_d = request.get_json()
    if not json_d:
        return jsonify({"error": "Not a JSON"}), 400
    name_s = json_d.get('name')
    if name_s is None:
        return jsonify({"error": "Missing name"}), 400
    new_s = Amenity(**json_d)
    new_s.save()
    return make_response(jsonify(new_s.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """Updates a Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    json_d = request.get_json()
    if not json_d:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in json_d.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict())
