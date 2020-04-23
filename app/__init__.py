#!/usr/bin/env python

"""
    Created by PyCharm
    ~~~~~~~~~~~
    :author: ilhamarrouf
    :date: 18/04/20
    :time: 08.26
"""

import os
from app.utils.storage import Minio
from flask import Flask, jsonify, request
from flask_caching import Cache
from flask_cors.extension import CORS
from flask_httpauth import HTTPBasicAuth
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_sqlalchemy import SQLAlchemy
from flasgger.base import Swagger


# Initialize core objects

app = Flask(__name__)
app.config.from_object("config")

cache = Cache(app)
cors = CORS(app)
db = SQLAlchemy(app)
auth = HTTPBasicAuth(app)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=[
        "100 per minute",
        "5 per second"
    ],
)
swagger = Swagger(app)
storage = Minio(app)

# -- Models
from app.models import user

if not os.path.exists("db.sqlite"):
    db.create_all()


# -- Controllers
from app.controllers import homepage_controller, \
    user_controller, \
    file_controller

app.register_blueprint(homepage_controller.mod)
app.register_blueprint(user_controller.mod)
app.register_blueprint(file_controller.mod)


# -- Error Handler
from app import errorhandler

