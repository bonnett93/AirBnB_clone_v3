#!/usr/bin/python3
"""start the flask"""

import os
from flask import Blueprint, render_template, abort
from flask_cors import CORS
from flask import Flask
from models import storage
from flask import jsonify
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)
cors = CORS(app, resources={"/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown(self):
    """calls storage.close()"""
    storage.close()


@app.errorhandler(404)
def page_not_found(error):
    """handler for 404 errors"""
    return (jsonify(error="Not found"), 404)

if __name__ == "__main__":
    make_h = os.getenv('HBNB_API_HOST', default='0.0.0.0')
    make_p = os.getenv('HBNB_API_PORT', default=5000)
    app.run(host=make_h, port=int(make_p), threaded=True)
