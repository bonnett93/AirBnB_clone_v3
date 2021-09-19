#!/usr/bin/python3
"""
Handles all default RESTFul API actions for State objects
"""

from flask import jsonify, abort, request, make_response
from api.v1.views import app_views
from models import storage
from models.user import User

@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """Retrieves the list of all State objects"""
    users = []
    for user in storage.all('User').values():
        users.append(user.to_dict())
    return jsonify(users)


@app_views.route('/users/<string:user_id>', methods=['GET'],
                 strict_slashes=False)
def user_id(user_id):
    """Retrieves a State object by id"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    else:
        return jsonify(user.to_dict())


@app_views.route('/users/<string:user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(user_id):
    """Deletes a State object"""
    user = storage.get(User, user_id)
    if use is None:
        abort(404)
    storage.delete(user)
    storage.save()
    empty = jsonify({})
    return (empty), 200

@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    """Creates a State"""
    json_d = request.get_json()
    if not json_d:
        return jsonify({"error": "Not a JSON"}), 400
    email = json_data.get("email")
    if email is None:
        return jsonify({"message": "Missing email"}), 400
    password = json_data.get("password")
    if password is None:
        return jsonify({"message": "Missing password"}), 400
    new_u = User(**json_d)
    new_u.save()
    return make_response(jsonify(new_u.to_dict()), 201)

@app_views.route('/users/<string:user_id>', methods=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """Updates a State object"""
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    json_d = request.get_json()
    if not json_d:
        return jsonify({"error": "Not a JSON"}), 400

    for key, value in json_d.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)

    storage.save()
    return jsonify(user.to_dict()), 200
