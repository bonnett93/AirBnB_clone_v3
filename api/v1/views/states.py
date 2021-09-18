#!/usr/bin/python3
"""
Contains the class DBStorage
"""

from flask import Blueprint, render_template, abort, request, make_response
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
from models.state import State

@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    states = []
    for state in storage.all('State').values():
        states.append(state.to_dict())
    return jsonify(states)

@app_views.route('/states/<string:state_id>', methods=['GET'], strict_slashes=False)
def state_id(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    else:
        return jsonify(state.to_dict())

@app_views.route('/states/<string:state_id>', methods=['DELETE'], strict_slashes=False)
def delete_state(state_id):
    state = storage.get('State', state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    empty = jsonify({})
    return (empty), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    json_d = request.get_json()
    if not json_d:
        return jsonify({"error": "Not a JSON"}), 400
    name_s = json_d.get('name')
    # name
    if name_s is None:
        return jsonify({"error": "Missing name"}), 400
    new_s = State(**json_d)
    new_s.save()
    return make_response(jsonify(new_s.do_dict()), 201)

@app_views.route('/states/<string:state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    state = storage.get('State', state_id)
    if state is None:
        # raise Http404
        abort (404)
    json_d = request.get_json()
    if not json_d:
        return jsonify({"error": "Not a JSON"}), 400

    # json_data x -> json_d
    for key, value in json_d.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, value)
    state.save()
    return jsonify(state.do_dict())
